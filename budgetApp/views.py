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
from datetime import datetime, timedelta

from .models import User, Categories, SubCategories, Account, Transaction

all_account = 0 # All account ID

def index(request):

    if request.user.is_authenticated:
        accounts = Account.objects.filter(userAccount=request.user)
        unread = Account.objects.filter(userAccount=request.user,read=False).count()
        isManyAccount = False
        balance = 0
        noOfAccounts = accounts.count()

        if noOfAccounts > 1 :
            for account in accounts:
                balance += account.balance
                isManyAccount = True

        for acc in accounts:
            acc.balance = currencyFormatter(acc.balance)
            acc.previousBalance = currencyFormatter(acc.previousBalance)

        return render(request, "budgetApp/index.html",{
            "accounts" : accounts,                      # Accounts informations
            "noOfAccounts": noOfAccounts,               # Number of accounts
            "isManyAccount" :  isManyAccount,           # Boolean if it is more that 1 accounts
            "balance": currencyFormatter(balance),      # Converts integer to currency
            "unread": unread                            # Return number of unread accounts
        })
    else: 
        return render(request, "budgetApp/login.html")

def transaction(request, id):
    
    # If all accounts clicked
    if id == all_account:
        transactions = Transaction.objects.filter(userTransaction=request.user)
        transactions = transactions.order_by("-transactionDate").all()

        for tran in transactions:
            tran.amount = currencyFormatter(tran.amount)
            tran.previousAccountBalance = currencyFormatter(tran.previousAccountBalance)
            tran.transactionDate = dateFormatter(tran.transactionDate)

    # Specific account is clicked
    else:
        transactions = Transaction.objects.filter(userTransaction=request.user,accountNameTransaction_id=id)
        transactions = transactions.order_by("-transactionDate").all()

        for tran in transactions:
            tran.amount = currencyFormatter(tran.amount)
            tran.previousAccountBalance = currencyFormatter(tran.previousAccountBalance)
            tran.transactionDate = dateFormatter(tran.transactionDate)

    return JsonResponse([transaction.serialize() for transaction in transactions], safe=False)

def unread(request, id):
    
    # If all accounts clicked
    if id == all_account :
        unread = Transaction.objects.filter(userTransaction=request.user,readTransaction=False)

        for read in unread:
            read.readTransaction = True
            read.save()

    # Specific account is clicked
    else: 
        unread = Transaction.objects.filter(userTransaction=request.user,accountNameTransaction_id=id,readTransaction=False)

        for read in unread:
            read.readTransaction = True
            read.save()

    return JsonResponse({"unread": unread.count()}, status=201)

def display(request, id):

    allAccount = True
    balance = 0
    # If all Accounts button is click 
    if id == all_account:
        account = Account.objects.filter(userAccount=request.user)
        accountRead = Account.objects.filter(userAccount=request.user)

        # Reads accounts
        for read in accountRead:
            read.read = True
            read.save()
        
        if account.count() > 1 :
            for acc in account:
                balance += acc.balance
        
        for acc in account:
            acc.balance = currencyFormatter(acc.balance)
            acc.previousBalance = currencyFormatter(acc.previousBalance)

    # Specific account is clicked
    else:
        allAccount = False
        account = Account.objects.get(userAccount=request.user,id=id)
        account.balance = currencyFormatter(account.balance)
        account.previousBalance = currencyFormatter(account.previousBalance)

        # Read account
        accountRead = Account.objects.get(userAccount=request.user,id=id)
        accountRead.read = True
        accountRead.save()
    
    return render(request, "budgetApp/display.html",{
        "account": account,
        "allAccount": allAccount,
        "balance": currencyFormatter(balance)
    })

def addTransaction(request):

    # Dropdown account, categories and subcategories data
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/addTransaction.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories
    })

def editTransaction(request, id):

    # Search for transaction will be edit
    transaction = Transaction.objects.get(userTransaction=request.user,id=id)
    transationDate = transaction.transactionDate.strftime("%Y/%m/%d")
    transationTime = transaction.transactionDate.strftime("%H:%M")
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/editTransaction.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories,
        "transaction" : transaction,
        "transationDate" : transationDate,
        "transationTime" : transationTime,
        "do": transaction.transactionType
    })

# Add credit transaction 
def creditAdd(request):
    
    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])

    credit = Transaction()
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = request.POST["accountName"]
    credit.transactionType = "credit"
    credit.amount = request.POST["amount"]
    credit.previousAccountBalance = account.balance
    credit.descriptionTransaction = request.POST["descriptions"]

    if request.POST["subCategory"] != "":
        category = request.POST["subCategory"].split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = request.POST["category"]

    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    credit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - int(request.POST["amount"])
    account.read = False
    account.save()

    return redirect('index')

# Edit credit transaction
def creditEdit(request, id):
    
    # Undo the previous data
    prevCredit = Transaction.objects.get(userTransaction=request.user,id=id)
    prevAccount = Account.objects.get(userAccount=request.user,id=prevCredit.accountNameTransaction_id)

    if prevCredit.transactionType == "credit":
        prevAccount.balance = prevAccount.balance + prevCredit.amount
    elif prevCredit.transactionType == "debit":
        prevAccount.balance = prevAccount.balance - prevCredit.amount

    prevAccount.read = False
    prevAccount.save()

    # Update the data with input data
    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])

    credit = Transaction.objects.get(userTransaction=request.user,id=id)
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = request.POST["accountName"]
    credit.transactionType = "credit"
    credit.amount = request.POST["amount"]
    credit.previousAccountBalance = account.balance
    credit.descriptionTransaction = request.POST["descriptions"]

    if request.POST["subCategory"] != "":
        category = request.POST["subCategory"].split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = request.POST["category"]

    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    credit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - int(request.POST["amount"])
    account.read = False
    account.save()

    return redirect('index')

# Add debit transaction
def debitAdd(request):
    
    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])

    debit = Transaction()
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = request.POST["accountName"]
    debit.transactionType = "debit"
    debit.amount = request.POST["amount"]
    debit.previousAccountBalance = account.balance
    debit.descriptionTransaction = request.POST["descriptions"]

    if request.POST["subCategory-debit"] != "":
        category = request.POST["subCategory-debit"].split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = request.POST["category-debit"]

    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    debit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + int(request.POST["amount"])
    account.read = False
    account.save()

    return redirect('index')

# Edit debit transaction
def debitEdit(request, id):
    
    # Undo the previous action
    prevDebit = Transaction.objects.get(userTransaction=request.user,id=id)
    prevAccount = Account.objects.get(userAccount=request.user,id=prevDebit.accountNameTransaction_id)

    if prevDebit.transactionType == "credit":
        prevAccount.balance = prevAccount.balance + prevDebit.amount
    elif prevDebit.transactionType == "debit":
        prevAccount.balance = prevAccount.balance - prevDebit.amount

    prevAccount.read = False
    prevAccount.save()

    # Update the data with current action
    account = Account.objects.get(userAccount=request.user,id=request.POST["accountName"])

    debit = Transaction.objects.get(userTransaction=request.user,id=id)
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = request.POST["accountName"]
    debit.transactionType = "debit"
    debit.amount = request.POST["amount"]
    debit.previousAccountBalance = account.balance
    debit.descriptionTransaction = request.POST["descriptions"]

    if request.POST["subCategory-debit"] != "":
        category = request.POST["subCategory-debit"].split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = request.POST["category-debit"]

    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    debit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + int(request.POST["amount"])
    account.read = False
    account.save()

    return redirect('index')

# Add transfering money to another account
def transferAdd(request):

    lastId = Transaction.objects.latest('id')
    
    accountFrom = Account.objects.get(userAccount=request.user,id=request.POST["accountNameFrom"])
    accountTo = Account.objects.get(userAccount=request.user,id=request.POST["accountNameTo"])

    # Account that will be deducted
    transfer = Transaction()
    transfer.id = lastId.id + 1
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.previousAccountBalance = accountFrom.balance
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.ins_date = datetime.now()
    transfer.save()

    # Destination account of transfer
    transfer = Transaction()
    transfer.id = lastId.id + 2
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameTo"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionFromId = lastId.id + 1
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.previousAccountBalance = accountTo.balance
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.ins_date = datetime.now()
    transfer.save()

    accountFrom.balance = accountFrom.balance - int(request.POST["amount"])
    accountFrom.read = False
    accountFrom.save()

    accountTo.balance = accountTo.balance + int(request.POST["amount"])
    accountTo.read = False
    accountTo.save()

    return redirect('index')

# Edit the added transfer transaction
def transferEdit(request, id):
    
    # Undo changes in accounts
    try:
        # When the origin account was about to edit
        # Destination account of money transfer
        prevTransfer = Transaction.objects.get(userTransaction=request.user,transactionFromId=id)
        accountFromId = id                                  # Origin account
        accountToId = prevTransfer.id                       # Destination account

    except:
        # When the destination account was about to edit
        # Origin account of money transfer
        prevTransfer = Transaction.objects.get(userTransaction=request.user,id=id)
        accountFromId = prevTransfer.transactionFromId      # Origin account
        accountToId = id                                    # Destination account

    prevAccountFrom = Account.objects.get(userAccount=request.user,id=prevTransfer.accountNameTransferFrom_id)
    prevAccountTo = Account.objects.get(userAccount=request.user,id=prevTransfer.accountNameTransferTo_id)
    prevAccountFrom.balance = prevAccountFrom.balance + prevTransfer.amount
    prevAccountTo.balance = prevAccountTo.balance - prevTransfer.amount

    prevAccountTo.read = False
    prevAccountTo.save()
    prevAccountFrom.read = False
    prevAccountFrom.save()


    # Update the data with current action
    accountFrom = Account.objects.get(userAccount=request.user,id=request.POST["accountNameFrom"])
    accountTo = Account.objects.get(userAccount=request.user,id=request.POST["accountNameTo"])

    # Account that will be deducted
    transfer = Transaction.objects.get(userTransaction=request.user,id=accountFromId)
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.previousAccountBalance = accountFrom.balance
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.save()

    # Destination account of transfer
    transfer = Transaction.objects.get(userTransaction=request.user,id=accountToId)
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = request.POST["accountNameTo"]
    transfer.accountNameTransferFrom_id = request.POST["accountNameFrom"]
    transfer.accountNameTransferTo_id = request.POST["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = request.POST["amount"]
    transfer.previousAccountBalance = accountTo.balance
    transfer.descriptionTransaction = request.POST["descriptions"]
    date = request.POST["transactionDate"]
    time = request.POST["transactionTime"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.save()

    accountFrom.balance = accountFrom.balance - int(request.POST["amount"])
    accountFrom.read = False
    accountFrom.save()

    accountTo.balance = accountTo.balance + int(request.POST["amount"])
    accountTo.read = False
    accountTo.save()

    return redirect('index')

# Settings
def settings(request):

    return render(request, "budgetApp/settings.html")

# Displays accounts in settings
def accounts(request):

    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")

    return render(request, "budgetApp/accounts.html",{
            "accounts" : accounts
        })

# Edit accounts 
def editAccount(request, id ):
    
    # Saving an edited data
    if request.method == "POST":
        accounts = Account.objects.get(id=id,userAccount=request.user)
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]
        accounts.previousBalance = accounts.balance
        accounts.balance = request.POST["balance"]
        accounts.read = False
        accounts.save()
        
        return redirect('accounts')
    
    # Display account information
    else :
        name = Account.objects.get(id=id)

        return render(request, "budgetApp/addEditAccount.html",{
            "name" : name,
            "id" : id,
            "do" : 'edit'
        })

# Adding an account
def addAccount(request):
    
    # Saving an added data
    if request.method == "POST":
        accounts = Account()
        accounts.userAccount = request.user
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]

        if request.POST["balance"] != "":
            accounts.balance = request.POST["balance"]
        else:
            accounts.balance = 0

        accounts.read = False
        accounts.previousBalance = 0
        accounts.save()

        return redirect('accounts')
    
    # Display add account html
    else :
        return render(request, "budgetApp/addEditAccount.html",{
            "do" : 'add'
        })

# Displays categories in settings
def categories(request):

    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/categories.html",{
            "categories" : categories,
            "subCategories" : subCategories
        })

# Edit category
def editCategory(request, id ):
    
    # Saving an edited data
    if request.method == "POST":
        category = Categories.objects.get(id=id,userCategory=request.user)
        category.category = request.POST["name"]
        category.save()

        return redirect('categories')

    # Displays the category html with data
    else :
        name = Categories.objects.get(id=id)
        categories = Categories.objects.all()

        return render(request, "budgetApp/addEditCategory.html",{
            "name" : name,
            "categories" : categories,
            "id" : id,
            "do" : 'edit',
            "class" : "category"
        })

# Edit a subcategory
def editSubCategory(request, id ):
    
    # Saving an edited data
    if request.method == "POST":
        subCategory = SubCategories.objects.get(id=id,userSubCategory=request.user)
        subCategory.parentCategory_id = request.POST["categoryList"]
        subCategory.subCategory = request.POST["name"]
        subCategory.save()

        return redirect('categories')

    # Displays the subcategory html with data
    else :
        name = SubCategories.objects.get(id=id)
        categories = Categories.objects.all()

        return render(request, "budgetApp/addEditCategory.html",{
            "name" : name,
            "categories" : categories,
            "id" : id,
            "do" : 'edit',
            "class" : "subCategory"
        })

# Adding a category
def addCategory(request):
    
    # Saving an added data
    if request.method == "POST":
        
        # If category list is not selected, it is an parent category 
        if request.POST["categoryList"] == "":
            category = Categories()
            category.userCategory = request.user
            category.category = request.POST["name"]
            category.save()

        # if category is selected, it is a subcategory
        else :
            subCategory = SubCategories()
            subCategory.userSubCategory = request.user
            subCategory.parentCategory_id = request.POST["categoryList"]
            subCategory.subCategory = request.POST["name"]
            subCategory.save()

        return redirect('categories')

    # Displays category html with data 
    else :
        categories = Categories.objects.all()

        return render(request, "budgetApp/addEditCategory.html",{
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

        except IntegrityError:
            return render(request, "budgetApp/register.html", {
                "message": "Username already taken."
            })

        login(request, user)

        return HttpResponseRedirect(reverse("index"))

    else:

        return render(request, "budgetApp/register.html")

# Formats the integer to currency
def currencyFormatter(amount):

    return "{:,}".format(amount)

# Formats the date
def dateFormatter(dateTrans):
    
    # Month day, year  
    if  dateTrans.strftime("%Y") < datetime.now().strftime("%Y") :

        return dateTrans.strftime("%B %d, %Y")

    date = datetime.now()  + timedelta(days=-7) 

    # Month day
    if  dateTrans.strftime("%B %d, %Y") < date.strftime("%B %d, %Y") :

        return dateTrans.strftime("%B %d")

    # Days of the week, Month day
    return dateTrans.strftime("%A, %B %d")