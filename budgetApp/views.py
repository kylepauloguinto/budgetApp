import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from django import forms
from django.shortcuts import redirect

from .models import User, Categories, SubCategories

def index(request):

    return render(request, "budgetApp/index.html")

def transaction(request):

    return render(request, "budgetApp/transaction.html")

def listCategories(request):

    categories = Categories.objects.order_by("category")
    subCategories = SubCategories.objects.order_by("subCategory")

    return render(request, "budgetApp/categories.html",{
            "categories" : categories,
            "subCategories" : subCategories
        })


def editCategory(request, id ):
    
    if request.method == "POST":
        category = Categories.objects.get(id=id,userCategory=request.user)
        category.category = request.POST["name"]
        category.save()
        
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()

        return redirect('listCategories')
    else :
        name = Categories.objects.filter(id=id)
        categories = Categories.objects.all()

        return render(request, "budgetApp/addEdit.html",{
            "name" : name[0],
            "categories" : categories,
            "id" : id,
            "do" : 'edit',
            "class" : "category"
        })

def editSubCategory(request, id ):
    
    if request.method == "POST":
        subCategory = SubCategories.objects.get(id=id,userSubCategory=request.user)
        subCategory.parentCategory_id = request.POST["categoryList"]
        subCategory.subCategory = request.POST["name"]
        subCategory.save()
        
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()

        return redirect('listCategories')
    else :
        name = SubCategories.objects.filter(id=id)
        categories = Categories.objects.all()

        return render(request, "budgetApp/addEdit.html",{
            "name" : name[0],
            "categories" : categories,
            "id" : id,
            "do" : 'edit',
            "class" : "subCategory"
        })


class NewTaskForm(forms.Form):
    category = forms.IntegerField(label="Category ID")

def addCategory(request):
    
    if request.method == "POST":
        if request.POST["categoryList"] == "":
            category = Categories()
            category.userCategory = request.user
            category.category = request.POST["name"]
            category.save()
        else :
            subCategory = SubCategories()
            subCategory.userSubCategory = request.user
            subCategory.parentCategory_id = request.POST["categoryList"]
            subCategory.subCategory = request.POST["name"]
            subCategory.save()
            
        categories = Categories.objects.all()
        subCategories = SubCategories.objects.all()

        return redirect('listCategories')
    else :
        categories = Categories.objects.all()
        return render(request, "budgetApp/addEdit.html",{
            "categories" : categories,
            "do" : 'add'
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "budgetApp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "budgetApp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "budgetApp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            #profile = Profile(
            #        userId=user
            #    )
            #profile.save()
        except IntegrityError:
            return render(request, "budgetApp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "budgetApp/register.html")