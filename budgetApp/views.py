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
from datetime import datetime

from .models import User, Categories, SubCategories, Account, Transaction

def index(request):

    accounts = Account.objects.filter(userAccount=request.user)

    return render(request, "budgetApp/index.html",{
        "accounts" : accounts
    })

def display(request, id):

    account = Account.objects.get(userAccount=request.user,id=id)
    transactions = Transaction.objects.filter(userTransaction=request.user,accountNameTransaction_id=id)
    transactions = transactions.order_by("-transactionDate").all()
    

    return render(request, "budgetApp/display.html",{
        "account": account,
        "transactions": transactions
    })

def transaction(request):

    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/transaction.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories
    })

def creditAdd(request):
    
    credit = Transaction()
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = request.POST["accountName"]
    credit.transactionType = "credit"
    credit.amount = request.POST["amount"]
    credit.descriptionTransaction = request.POST["descriptions"]
    if request.POST["subCategory"] != "":
        category = request.POST["subCategory"].split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = request.POST["classification"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    credit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")

    credit.save()

    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])
    account.balance = account.balance - int(request.POST["amount"])
    account.save()

    return redirect('index')

def debitAdd(request):
    
    debit = Transaction()
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = request.POST["accountName"]
    debit.transactionType = "debit"
    debit.amount = request.POST["amount"]
    debit.descriptionTransaction = request.POST["descriptions"]
    if request.POST["subCategory-debit"] != "":
        category = request.POST["subCategory-debit"].split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = request.POST["classification-debit"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    debit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")

    debit.save()

    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])
    account.balance = account.balance + int(request.POST["amount"])
    account.save()

    return redirect('index')

def transferAdd(request):
    
    #account that will be deducted
    transfer = Transaction()
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")

    transfer.save()

    #account that amount will be transfer
    transfer = Transaction()
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameTo"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")

    transfer.save()

    accountFrom = Account.objects.get(userAccount=request.user,id=request.POST["accountNameFrom"])
    accountFrom.balance = accountFrom.balance - int(request.POST["amount"])
    accountFrom.save()

    accountTo = Account.objects.get(userAccount=request.user,id=request.POST["accountNameTo"])
    accountTo.balance = accountTo.balance + int(request.POST["amount"])
    accountTo.save()

    return redirect('index')

def settings(request):

    return render(request, "budgetApp/settings.html")

def accounts(request):

    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")

    return render(request, "budgetApp/accounts.html",{
            "accounts" : accounts
        })

def editAccount(request, id ):
    
    if request.method == "POST":
        accounts = Account.objects.get(id=id,userAccount=request.user)
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]
        accounts.save()
        
        return redirect('accounts')
    else :
        name = Account.objects.filter(id=id)

        return render(request, "budgetApp/addEditAccount.html",{
            "name" : name[0],
            "id" : id,
            "do" : 'edit'
        })

def addAccount(request):
    
    if request.method == "POST":
        accounts = Account()
        accounts.userAccount = request.user
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]
        accounts.balance = 0
        accounts.save()

        return redirect('accounts')
    else :
        return render(request, "budgetApp/addEditAccount.html",{
            "do" : 'add'
        })

def categories(request):

    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/categories.html",{
            "categories" : categories,
            "subCategories" : subCategories
        })


def editCategory(request, id ):
    
    if request.method == "POST":
        category = Categories.objects.get(id=id,userCategory=request.user)
        category.category = request.POST["name"]
        category.save()

        return redirect('categories')
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

        return redirect('categories')
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

        return redirect('categories')
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