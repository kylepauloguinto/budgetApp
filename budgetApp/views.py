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

def transaction(request, id, pageNo):
    
    # If all accounts clicked
    if id == all_account:
        transactions = Transaction.objects.filter(userTransaction=request.user)
        transactions = transactions.order_by("-transactionDate").all()
        transactions = Paginator(transactions,10)
        transactions = transactions.page(pageNo).object_list

        for tran in transactions:
            tran.amount = currencyFormatter(tran.amount)
            tran.previousAccountBalance = currencyFormatter(tran.previousAccountBalance)
            tran.transactionDate = dateFormatter(tran.transactionDate)

    # Specific account is clicked
    else:
        transactions = Transaction.objects.filter(userTransaction=request.user,accountNameTransaction_id=id)
        transactions = transactions.order_by("-transactionDate").all()
        transactions = Paginator(transactions,10)
        transactions = transactions.page(pageNo).object_list

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

def addTransaction(request,id):

    # Dropdown account, categories and subcategories data
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")

    return render(request, "budgetApp/addTransaction.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories,
        "date": datetime.now().strftime("%Y/%m/%d"),
        "time": datetime.now().strftime("%H:%M"),
        "do": "credit",
        "accountId": id
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
        "do": transaction.transactionType,
        "accountId": transaction.accountNameTransaction_id
    })

# Add credit transaction
@csrf_exempt
@login_required
def creditAdd(request, id):
    
    messageList = validation(request, "credit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

    account = Account.objects.get(userAccount=request.user,id=data["accountName"])

    credit = Transaction()
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = data["accountName"]
    credit.transactionType = "credit"
    credit.amount = data["amount"]
    credit.previousAccountBalance = account.balance
    credit.descriptionTransaction = data["description"]

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = data["category"]

    date = data["date"]
    time = data["time"]
    credit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - int(data["amount"])
    account.read = False
    account.save()

    return JsonResponse({"message": "success"}, status=200)

# Edit credit transaction
@csrf_exempt
@login_required
def creditEdit(request, id):
    
    messageList = validation(request, "credit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

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
    account = Account.objects.get(userAccount=request.user,id=data["accountName"])

    credit = Transaction.objects.get(userTransaction=request.user,id=id)
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = data["accountName"]
    credit.transactionType = "credit"
    credit.amount = data["amount"]
    credit.previousAccountBalance = account.balance
    credit.descriptionTransaction = data["description"]

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = data["category"]

    date = data["date"]
    time = data["time"]
    credit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - int(data["amount"])
    account.read = False
    account.save()

    return JsonResponse({"message": "success"}, status=200)

# Add debit transaction
@csrf_exempt
@login_required
def debitAdd(request, id):
    
    messageList = validation(request, "debit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

    account = Account.objects.get(userAccount=request.user,id=data["accountName"])

    debit = Transaction()
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = data["accountName"]
    debit.transactionType = "debit"
    debit.amount = data["amount"]
    debit.previousAccountBalance = account.balance
    debit.descriptionTransaction = data["description"]

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = data["category"]

    date = data["date"]
    time = data["time"]
    debit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + int(data["amount"])
    account.read = False
    account.save()

    return JsonResponse({"message": "success"}, status=200)

# Edit debit transaction
@csrf_exempt
@login_required
def debitEdit(request, id):
    
    messageList = validation(request, "debit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

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
    account = Account.objects.get(userAccount=request.user,id=data["accountName"])

    debit = Transaction.objects.get(userTransaction=request.user,id=id)
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = data["accountName"]
    debit.transactionType = "debit"
    debit.amount = data["amount"]
    debit.previousAccountBalance = account.balance
    debit.descriptionTransaction = data["description"]

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = data["category"]

    date = data["date"]
    time = data["time"]
    debit.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + int(data["amount"])
    account.read = False
    account.save()

    return JsonResponse({"message": "success"}, status=200)

# Add transfering money to another account
@csrf_exempt
@login_required
def transferAdd(request, id):
    
    messageList = validation(request, "transfer")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

    lastId = Transaction.objects.latest('id')
    
    accountFrom = Account.objects.get(userAccount=request.user,id=data["accountNameFrom"])
    accountTo = Account.objects.get(userAccount=request.user,id=data["accountNameTo"])

    # Account that will be deducted
    transfer = Transaction()
    transfer.id = lastId.id + 1
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = data["accountNameFrom"]
    transfer.accountNameTransferFrom_id = data["accountNameFrom"]
    transfer.accountNameTransferTo_id = data["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = data["amount"]
    transfer.previousAccountBalance = accountFrom.balance
    transfer.descriptionTransaction = data["description"]
    date = data["date"]
    time = data["time"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.ins_date = datetime.now()
    transfer.save()

    # Destination account of transfer
    transfer = Transaction()
    transfer.id = lastId.id + 2
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = data["accountNameTo"]
    transfer.accountNameTransferFrom_id = data["accountNameFrom"]
    transfer.accountNameTransferTo_id = data["accountNameTo"]
    transfer.transactionFromId = lastId.id + 1
    transfer.transactionType = "transfer"
    transfer.amount = data["amount"]
    transfer.previousAccountBalance = accountTo.balance
    transfer.descriptionTransaction = data["description"]
    date = data["date"]
    time = data["time"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.ins_date = datetime.now()
    transfer.save()

    accountFrom.balance = accountFrom.balance - int(data["amount"])
    accountFrom.read = False
    accountFrom.save()

    accountTo.balance = accountTo.balance + int(data["amount"])
    accountTo.read = False
    accountTo.save()

    return JsonResponse({"message": "success"}, status=200)

# Edit the added transfer transaction
@csrf_exempt
@login_required
def transferEdit(request, id):
    
    messageList = validation(request, "transfer")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

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
    accountFrom = Account.objects.get(userAccount=request.user,id=data["accountNameFrom"])
    accountTo = Account.objects.get(userAccount=request.user,id=data["accountNameTo"])

    # Account that will be deducted
    transfer = Transaction.objects.get(userTransaction=request.user,id=accountFromId)
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = data["accountNameFrom"]
    transfer.accountNameTransferFrom_id = data["accountNameFrom"]
    transfer.accountNameTransferTo_id = data["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = data["amount"]
    transfer.previousAccountBalance = accountFrom.balance
    transfer.descriptionTransaction = data["description"]
    date = data["date"]
    time = data["time"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.save()

    # Destination account of transfer
    transfer = Transaction.objects.get(userTransaction=request.user,id=accountToId)
    transfer.userTransaction = request.user
    transfer.accountNameTransaction_id = data["accountNameTo"]
    transfer.accountNameTransferFrom_id = data["accountNameFrom"]
    transfer.accountNameTransferTo_id = data["accountNameTo"]
    transfer.transactionType = "transfer"
    transfer.amount = data["amount"]
    transfer.previousAccountBalance = accountTo.balance
    transfer.descriptionTransaction = data["description"]
    date = data["date"]
    time = data["time"]
    transfer.transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    transfer.readTransaction = False
    transfer.save()

    accountFrom.balance = accountFrom.balance - int(data["amount"])
    accountFrom.read = False
    accountFrom.save()

    accountTo.balance = accountTo.balance + int(data["amount"])
    accountTo.read = False
    accountTo.save()

    return JsonResponse({"message": "success"}, status=200)

# Delete Transaction
@csrf_exempt
@login_required
def deleteTransaction(request, id):

    data = json.loads(request.body)
    item = data["item"]
    balance = 0
    trans = ""

    if Transaction.objects.filter(userTransaction=request.user,transactionFromId=item).exists():
        transferTo = Transaction.objects.get(userTransaction=request.user,transactionFromId=item)
        transferFrom = Transaction.objects.get(userTransaction=request.user,id=item)

        # To return data
        transaction = Transaction.objects.filter(userTransaction=request.user,transactionFromId=item)
        trans = [trans.serialize() for trans in transaction]

        accountFrom = Account.objects.get(userAccount=request.user,id=transferTo.accountNameTransferFrom_id)
        accountTo = Account.objects.get(userAccount=request.user,id=transferTo.accountNameTransferTo_id)

        accountFrom.balance = accountFrom.balance + transferTo.amount
        accountFrom.read = False
        accountFrom.save()
        
        accountTo.balance = accountTo.balance - transferTo.amount
        accountTo.read = False
        accountTo.save()

        transferFrom.delete()
        transferTo.delete()
        
        # For all accounts process
        if id == 0:
            accounts = Account.objects.filter(userAccount=request.user).all()
            for account in accounts:
                balance += account.balance
        else:
            account = Account.objects.get(userAccount=request.user,id=id)
            balance = account.balance
    else:
        transaction = Transaction.objects.get(userTransaction=request.user,id=item)
        transactionType = transaction.transactionType
        
        # To return data
        getData = Transaction.objects.filter(userTransaction=request.user,id=item)
        trans = [trans.serialize() for trans in getData]

        if transactionType == "transfer":
            transferTo = Transaction.objects.get(userTransaction=request.user,id=item)
            transferFrom = Transaction.objects.get(userTransaction=request.user,id=transferTo.transactionFromId)

            accountFrom = Account.objects.get(userAccount=request.user,id=transferTo.accountNameTransferFrom_id)
            accountTo = Account.objects.get(userAccount=request.user,id=transferTo.accountNameTransferTo_id)

            accountFrom.balance = accountFrom.balance + transferTo.amount
            accountFrom.read = False
            accountFrom.save()

            accountTo.balance = accountTo.balance - transferTo.amount
            accountTo.read = False
            accountTo.save()

            transferFrom.delete()
            transferTo.delete()
            
            # For all accounts process
            if id == 0:
                accounts = Account.objects.filter(userAccount=request.user).all()
                for account in accounts:
                    balance += account.balance
            else:
                account = Account.objects.get(userAccount=request.user,id=id)
                balance = account.balance

        elif transactionType == "credit":
            credit = Transaction.objects.get(userTransaction=request.user,id=item)
            
            account = Account.objects.get(userAccount=request.user,id=credit.accountNameTransaction_id)
            account.balance = account.balance + credit.amount
            account.read = False
            account.save()

            credit.delete()
            
            # For all accounts process
            if id == 0:
                accounts = Account.objects.filter(userAccount=request.user).all()
                for account in accounts:
                    balance += account.balance
            else:
                balance = account.balance

        elif transactionType == "debit":
            debit = Transaction.objects.get(userTransaction=request.user,id=item)
            
            account = Account.objects.get(userAccount=request.user,id=debit.accountNameTransaction_id)
            account.balance = account.balance - debit.amount
            account.read = False
            account.save()

            debit.delete()
            
            # For all accounts process
            if id == 0:
                accounts = Account.objects.filter(userAccount=request.user).all()
                for account in accounts:
                    balance += account.balance
            else:
                balance = account.balance

    return JsonResponse({"message": "success", "balance": balance , "data": trans}, status=200)

# Settings
def settings(request):

    return render(request, "budgetApp/settings.html")

# Displays accounts in settings
def accounts(request):

    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")

    return render(request, "budgetApp/accounts.html",{
            "accounts" : accounts
        })

# Delete account
@csrf_exempt
@login_required
def deleteAccount(request):
    
    data = json.loads(request.body)
    try:
        accounts = Account.objects.get(userAccount=request.user,id=data["item"])
        accounts.delete()
    except:
        return JsonResponse({"message": "error"}, status=500)

    return JsonResponse({"message": "success"}, status=200)
        
# Edit accounts 
def editAccount(request, id ):
    
    # Saving an edited data
    if request.method == "POST":
        
        # Validation
        message = False
        accountNameError = False
        balanceError = False
        descriptionError = False
        accountNameErrMes = ""
        balanceErrMes = ""
        descriptionErrMes = ""
        accountName = request.POST["accountName"]
        description = request.POST["description"]
        balance = request.POST["balance"]

        if accountName == "":
            accountNameErrMes = "Please input an account name."
            accountNameError = True
            message = True
        
        if accountName is not None and len(accountName) > 10:
            accountNameErrMes = "Please input an account name within 10 letters."
            accountNameError = True
            message = True
                
        if description == "":
            descriptionErrMes = "Please input a description."
            descriptionError = True
            message = True
        
        if description is not None and len(description) > 15:
            descriptionErrMes = "Please input a description within 15 letters."
            descriptionError = True
            message = True
        
        if balance.find(".") > 0 :
            balanceErrMes = "Please input integer number."
            balanceError = True
            message = True

        if message :
            return render(request, "budgetApp/editAccount.html",{
                "id" : id,
                "message": message,
                "accountName" : accountName,
                "description" : description,
                "balance" : balance,
                "accountNameError": accountNameError,
                "accountNameErrMes": accountNameErrMes,
                "balanceError": balanceError,
                "balanceErrMes": balanceErrMes,
                "descriptionError": descriptionError,
                "descriptionErrMes": descriptionErrMes
            })

        # Validation success
        accounts = Account.objects.get(id=id,userAccount=request.user)
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]
        accounts.previousBalance = accounts.balance
        
        if balance == "":
            balance = accounts.balance

        accounts.balance = balance
        accounts.read = False
        accounts.save()
        
        return redirect('accounts')
    
    # Display account information
    else :
        account = Account.objects.get(id=id)
        accountName = account.accountName
        description = account.description
        balance = account.balance

        return render(request, "budgetApp/editAccount.html",{
            "accountName" : accountName,
            "description" : description,
            "balance" : balance,
            "id" : id
        })

# Adding an account
def addAccount(request):
    
    # Saving an added data
    if request.method == "POST":

        # Validation
        message = False
        accountNameError = False
        balanceError = False
        descriptionError = False
        accountNameErrMes = ""
        balanceErrMes = ""
        descriptionErrMes = ""
        accountName = request.POST["accountName"]
        description = request.POST["description"]
        balance = request.POST["balance"]

        if accountName == "":
            accountNameErrMes = "Please input an account name."
            accountNameError = True
            message = True
        
        if accountName is not None and len(accountName) > 10:
            accountNameErrMes = "Please input an account name within 10 letters."
            accountNameError = True
            message = True
                
        if description == "":
            descriptionErrMes = "Please input a description."
            descriptionError = True
            message = True
        
        if description is not None and len(description) > 15:
            descriptionErrMes = "Please input a description within 15 letters."
            descriptionError = True
            message = True
        
        if balance.find(".") > 0 :
            balanceErrMes = "Please input integer number."
            balanceError = True
            message = True

        if message :
            return render(request, "budgetApp/addAccount.html",{
                "message": message,
                "accountName" : accountName,
                "description" : description,
                "balance" : balance,
                "accountNameError": accountNameError,
                "accountNameErrMes": accountNameErrMes,
                "balanceError": balanceError,
                "balanceErrMes": balanceErrMes,
                "descriptionError": descriptionError,
                "descriptionErrMes": descriptionErrMes
            })

        # Validation success
        accounts = Account()
        accounts.userAccount = request.user
        accounts.accountName = accountName
        accounts.description = description

        if balance != "":
            accounts.balance = balance
        else:
            accounts.balance = 0

        accounts.read = False
        accounts.previousBalance = 0
        accounts.save()

        return redirect('accounts')
    
    # Display add account html
    else :
        return render(request, "budgetApp/addAccount.html")

# Delete categories
@csrf_exempt
@login_required
def deleteCategory(request):
    
    data = json.loads(request.body)
    try:
        categories = Categories.objects.get(userCategory=request.user,id=data["item"])
        categories.delete()
    except:
        return JsonResponse({"message": "error"}, status=500)

    return JsonResponse({"message": "success"}, status=200)

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

        # Validation
        message = False
        nameError = False
        nameErrMes = ""
        name = request.POST["name"]

        if name == "":
            nameErrMes = "Please input an account name."
            nameError = True
            message = True
        
        if name is not None and len(name) > 15:
            nameErrMes = "Please input an account name within 15 letters."
            nameError = True
            message = True

        if message :
            categories = Categories.objects.filter(userCategory=request.user).all()

            return render(request, "budgetApp/editCategory.html",{
                "id" : id,
                "class" : "category",
                "categories" : categories,
                "name": name,
                "nameError": nameError,
                "nameErrMes": nameErrMes
            })

        # Validation success
        category = Categories.objects.get(id=id,userCategory=request.user)
        category.category = name
        category.save()

        return redirect('categories')

    # Displays the category html with data
    else :
        name = Categories.objects.get(userCategory=request.user,id=id)
        categories = Categories.objects.filter(userCategory=request.user).all()

        return render(request, "budgetApp/editCategory.html",{
            "name" : name,
            "categories" : categories,
            "id" : id,
            "class" : "category"
        })

# Delete subcategories
@csrf_exempt
@login_required
def deleteSubcategory(request):
    
    data = json.loads(request.body)
    try:
        subcategories = SubCategories.objects.get(userSubCategory=request.user,id=data["item"])
        subcategories.delete()
    except:
        return JsonResponse({"message": "error"}, status=500)

    return JsonResponse({"message": "success"}, status=200)

# Edit a subcategory
def editSubCategory(request, id ):
    
    # Saving an edited data
    if request.method == "POST":
        
        # Validation
        message = False
        nameError = False
        nameErrMes = ""
        categoryError = False
        categoryErrMes = ""
        name = request.POST["name"]
        category = request.POST["categoryList"]

        if name == "":
            nameErrMes = "Please input an account name."
            nameError = True
            message = True
        
        if name is not None and len(name) > 15:
            nameErrMes = "Please input an account name within 15 letters."
            nameError = True
            message = True
        
        if category != "" and not Categories.objects.filter(userCategory=request.user,id=category).exists():
            categoryErrMes = "Selected category is not exists."
            categoryError = True
            message = True

        if message :
            categories = Categories.objects.filter(userCategory=request.user).all()

            return render(request, "budgetApp/editCategory.html",{
                "id" : id,
                "class" : "subCategory",
                "categories" : categories,
                "name": name,
                "nameError": nameError,
                "nameErrMes": nameErrMes,
                "parentCategory": int(category) if category != "" else "",
                "categoryError": categoryError,
                "categoryErrMes": categoryErrMes
            })

        # If category list is not selected, it is an parent category 
        if request.POST["categoryList"] == "":
            category = Categories()
            category.userCategory = request.user
            category.category = request.POST["name"]
            category.save()

            subCategory = SubCategories.objects.get(id=id,userSubCategory=request.user)
            subCategory.delete()

        # if category is selected, it is a subcategory
        else :
            # Validation success
            subCategory = SubCategories.objects.get(id=id,userSubCategory=request.user)
            subCategory.parentCategory_id = request.POST["categoryList"]
            subCategory.subCategory = request.POST["name"]
            subCategory.save()
            

        return redirect('categories')

    # Displays the subcategory html with data
    else :
        name = SubCategories.objects.get(userSubCategory=request.user,id=id)
        categories = Categories.objects.filter(userCategory=request.user).all()

        return render(request, "budgetApp/editCategory.html",{
            "name" : name.subCategory,
            "parentCategory": int(name.parentCategory.id),
            "categories" : categories,
            "id" : id,
            "class" : "subCategory"
        })

# Adding a category
def addCategory(request):
    
    # Saving an added data
    if request.method == "POST":
        
        # Validation
        message = False
        nameError = False
        nameErrMes = ""
        categoryError = False
        categoryErrMes = ""
        name = request.POST["name"]
        category = request.POST["categoryList"]

        if name == "":
            nameErrMes = "Please input an account name."
            nameError = True
            message = True
        
        if name is not None and len(name) > 15:
            nameErrMes = "Please input an account name within 15 letters."
            nameError = True
            message = True
        
        if category != "" and not Categories.objects.filter(userCategory=request.user,id=category).exists():
            categoryErrMes = "Selected category is not exists."
            categoryError = True
            message = True

        if message :
            categories = Categories.objects.filter(userCategory=request.user).all()

            return render(request, "budgetApp/addCategory.html",{
                "categories" : categories,
                "name": name,
                "nameError": nameError,
                "nameErrMes": nameErrMes,
                "categoryVal": int(category) if category != "" else "",
                "categoryError": categoryError,
                "categoryErrMes": categoryErrMes
            })

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
        categories = Categories.objects.filter(userCategory=request.user).all()

        return render(request, "budgetApp/addCategory.html",{
            "categories" : categories
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

# Validations
def validation(request, action):
    data = json.loads(request.body)
    messageList = []
    amount = data.get("amount")
    description = data.get("description")

    # Amount
    if amount == "":
        messageList.append({"id":"amount", "message":"Please input amount."})

    if amount.find(".") > 0 :
        messageList.append({"id":"amount", "message":"Please input integer number."})
    
    if amount is not None and len(amount) > 15:
        messageList.append({"id":"amount", "message":"Please input amount within 15 numbers."})

    # Description
    if description is not None and len(description) > 25:
        messageList.append({"id":"description", "message":"Please input description within 25 letters."})
    
    if action != "transfer":

        # Category and Subcategory
        category = data.get("category")
        subCategory = data.get("subcategory")
        parentSubCategory = ""
        parentExists = True

        if subCategory != "" and subCategory != None:
            subCategory = subCategory.split("-")
            parentSubCategory = subCategory[0]
            subCategory = subCategory[1]

        if category != "" and not Categories.objects.filter(userCategory=request.user,id=category).exists():
            messageList.append({"id":"category", "message":"Selected category is not exists."})

        if subCategory != "" and subCategory != None and not SubCategories.objects.filter(userSubCategory=request.user,parentCategory_id=parentSubCategory).exists():
            messageList.append({"id":"subCategory", "message":"Selected subcategory has no parent category."})
            parentExists = False

        if subCategory != "" and subCategory != None and parentExists and not SubCategories.objects.filter(userSubCategory=request.user,id=subCategory).exists():
            messageList.append({"id":"subCategory", "message":"Selected subcategory is not exists."})


        # Account
        accountName = data.get("accountName")
        
        if accountName == "":
            messageList.append({"id":"accountName", "message":"Please input account."})
        
        if accountName != "" and not Account.objects.filter(userAccount=request.user,id=accountName).exists():
            messageList.append({"id":"accountName", "message":"Account is not exists."})
    else:
        accountFrom = data.get("accountNameFrom")
        accountTo = data.get("accountNameTo")
        
        if accountFrom == "":
            messageList.append({"id":"accountNameFrom", "message":"Please input account from."})
            
        if not accountTo:
            messageList.append({"id":"accountNameTo", "message":"Please input account to."})
        
        if accountFrom != "" and not Account.objects.filter(userAccount=request.user,id=accountFrom).exists():
            messageList.append({"id":"accountNameFrom", "message":"Account selected is not exists."})

        if accountTo and not Account.objects.filter(userAccount=request.user,id=accountTo).exists():
            messageList.append({"id":"accountNameTo", "message":"Account selected is not exists."})


    return messageList