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
from datetime import  date, datetime, timedelta
import calendar

from .models import User, Categories, SubCategories, Account, Transaction, Budget

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
        transactions = transactions.order_by("-transactionDate","-id").all()
        transactions = Paginator(transactions,10)
        transactions = transactions.page(pageNo).object_list

        for tran in transactions:
            tran.amount = currencyFormatter(tran.amount)
            tran.previousAccountBalance = currencyFormatter(tran.previousAccountBalance)
            tran.transactionDate = dateFormatter(tran.transactionDate)

    # Specific account is clicked
    else:
        transactions = Transaction.objects.filter(userTransaction=request.user,accountNameTransaction_id=id)
        transactions = transactions.order_by("-transactionDate","-id").all()
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

    accountName = data["accountName"]
    description = data["description"]
    amount = int(data["amount"])
    category = data["category"]
    subcategory = data["subcategory"]

    # credit process
    account = Account.objects.get(userAccount=request.user,id=accountName)

    credit = Transaction()
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = accountName
    credit.transactionType = "credit"
    credit.amount = amount
    credit.previousAccountBalance = account.balance
    credit.currentAccountBalance = account.balance - amount
    credit.descriptionTransaction = description

    if subcategory != "":
        category = subcategory.split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = category

    date = data["date"]
    time = data["time"] 
    transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.transactionDate = transactionDate
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - amount
    account.read = False
    account.save()

    # budget process
    budgets = []

    if subcategory != "":
        budgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=accountName,
                                    subCategoryBudget_id=category[1],
                                    startDate__lte=transactionDate,
                                    endDate__gte=transactionDate)
    elif category != "":
        budgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=accountName,
                                    categoryBudget_id=category,
                                    subCategoryBudget__isnull=True,
                                    startDate__lte=transactionDate,
                                    endDate__gte=transactionDate)

    for budget in budgets:
        budget.currentAmount += amount

        diff = int(budget.budgetAmount) - int(budget.currentAmount)
        if diff < 0:
            budget.minusAmount = True
        else:
            budget.minusAmount = False
        budget.save()

    return JsonResponse({"message": "success"}, status=200)

# Edit credit transaction
@csrf_exempt
@login_required
def creditEdit(request, id):
    
    messageList = validation(request, "credit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

    accountName = data["accountName"]
    description = data["description"]
    amount = int(data["amount"])
    category = data["category"]
    subcategory = data["subcategory"]

    # Undo the previous data
    prevCredit = Transaction.objects.get(userTransaction=request.user,id=id)
    prevAccount = Account.objects.get(userAccount=request.user,id=prevCredit.accountNameTransaction_id)
    prevBudgets = []

    if prevCredit.subCategoryTransaction_id != "" and prevCredit.subCategoryTransaction_id is not None:
        prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=prevCredit.accountNameTransaction_id,
                                    subCategoryBudget_id=prevCredit.subCategoryTransaction_id,
                                    startDate__lte=prevCredit.transactionDate,
                                    endDate__gte=prevCredit.transactionDate)
    elif prevCredit.categoryTransaction_id != "" and prevCredit.categoryTransaction_id is not None:
        prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=prevCredit.accountNameTransaction_id,
                                    categoryBudget_id=prevCredit.categoryTransaction_id,
                                    subCategoryBudget__isnull=True,
                                    startDate__lte=prevCredit.transactionDate,
                                    endDate__gte=prevCredit.transactionDate)
    if prevCredit.transactionType == "credit":
        prevAccount.balance = prevAccount.balance + prevCredit.amount
        
        for budget in prevBudgets:
            currentAmount = budget.currentAmount - prevCredit.amount

            if currentAmount <= 0:
                currentAmount = 0

            budget.currentAmount = currentAmount
            diff = int(budget.budgetAmount) - int(budget.currentAmount)
            if diff < 0:
                budget.minusAmount = True
            else:
                budget.minusAmount = False
            budget.save()

    elif prevCredit.transactionType == "debit":
        prevAccount.balance = prevAccount.balance - prevCredit.amount

    prevAccount.read = False
    prevAccount.save()

    # Update the data with input data
    account = Account.objects.get(userAccount=request.user,id=accountName)

    credit = Transaction.objects.get(userTransaction=request.user,id=id)
    credit.userTransaction = request.user
    credit.accountNameTransaction_id = accountName
    credit.transactionType = "credit"
    credit.amount = amount
    credit.previousAccountBalance = account.balance
    credit.currentAccountBalance = account.balance - amount
    credit.descriptionTransaction = description

    if subcategory != "":
        category = subcategory.split("-")
        credit.categoryTransaction_id = category[0]
        credit.subCategoryTransaction_id = category[1]
    else:
        credit.categoryTransaction_id = category
        credit.subCategoryTransaction_id = ""

    date = data["date"]
    time = data["time"]
    transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    credit.transactionDate = transactionDate
    credit.readTransaction = False
    credit.save()

    account.balance = account.balance - amount
    account.read = False
    account.save()

    # budget process
    budgets = []

    if subcategory != "":
        budgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=accountName,
                                    subCategoryBudget_id=category[1],
                                    startDate__lte=transactionDate,
                                    endDate__gte=transactionDate)
    elif category != "":
        budgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=accountName,
                                    categoryBudget_id=category,
                                    subCategoryBudget__isnull=True,
                                    startDate__lte=transactionDate,
                                    endDate__gte=transactionDate)
    
    for budget in budgets:
        budget.currentAmount += amount

        diff = int(budget.budgetAmount) - int(budget.currentAmount)
        if diff < 0:
            budget.minusAmount = True
        else:
            budget.minusAmount = False
        budget.save()

    return JsonResponse({"message": "success"}, status=200)

# Add debit transaction
@csrf_exempt
@login_required
def debitAdd(request, id):
    
    messageList = validation(request, "debit")
    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    data = json.loads(request.body)

    accountName = data["accountName"]
    description = data["description"]
    amount = int(data["amount"])
    category = data["category"]
    subcategory = data["subcategory"]

    # debit process
    account = Account.objects.get(userAccount=request.user,id=accountName)

    debit = Transaction()
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = accountName
    debit.transactionType = "debit"
    debit.amount = amount
    debit.previousAccountBalance = account.balance
    debit.currentAccountBalance = account.balance + amount
    debit.descriptionTransaction = description

    if subcategory != "":
        category = subcategory.split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = category

    date = data["date"]
    time = data["time"]
    transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.transactionDate = transactionDate
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + amount
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

    accountName = data["accountName"]
    description = data["description"]
    amount = int(data["amount"])
    category = data["category"]
    subcategory = data["subcategory"]

    # Undo the previous action
    prevDebit = Transaction.objects.get(userTransaction=request.user,id=id)
    prevAccount = Account.objects.get(userAccount=request.user,id=prevDebit.accountNameTransaction_id)
    prevBudgets = []

    if prevDebit.subCategoryTransaction_id != "" and prevDebit.subCategoryTransaction_id is not None:
        prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=prevDebit.accountNameTransaction_id,
                                    subCategoryBudget_id=prevDebit.subCategoryTransaction_id,
                                    startDate__lte=prevDebit.transactionDate,
                                    endDate__gte=prevDebit.transactionDate)
    elif prevDebit.categoryTransaction_id != "" and prevDebit.categoryTransaction_id is not None:
        prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=prevDebit.accountNameTransaction_id,
                                    categoryBudget_id=prevDebit.categoryTransaction_id,
                                    subCategoryBudget__isnull=True,
                                    startDate__lte=prevDebit.transactionDate,
                                    endDate__gte=prevDebit.transactionDate)

    if prevDebit.transactionType == "credit":
        prevAccount.balance = prevAccount.balance + prevDebit.amount

        for budget in prevBudgets:
            currentAmount = budget.currentAmount - prevDebit.amount

            if currentAmount <= 0:
                currentAmount = 0

            budget.currentAmount = currentAmount

            diff = int(budget.budgetAmount) - int(budget.currentAmount)
            if diff < 0:
                budget.minusAmount = True
            else:
                budget.minusAmount = False
            budget.save()

    elif prevDebit.transactionType == "debit":
        prevAccount.balance = prevAccount.balance - prevDebit.amount

    prevAccount.read = False
    prevAccount.save()

    # Update the data with current action
    account = Account.objects.get(userAccount=request.user,id=accountName)

    debit = Transaction.objects.get(userTransaction=request.user,id=id)
    debit.userTransaction = request.user
    debit.accountNameTransaction_id = accountName
    debit.transactionType = "debit"
    debit.amount = amount
    debit.previousAccountBalance = account.balance
    debit.currentAccountBalance = account.balance + amount
    debit.descriptionTransaction = description

    if subcategory != "":
        category = subcategory.split("-")
        debit.categoryTransaction_id = category[0]
        debit.subCategoryTransaction_id = category[1]
    else:
        debit.categoryTransaction_id = category
        debit.subCategoryTransaction_id = ""

    date = data["date"]
    time = data["time"]
    transactionDate = datetime.strptime(date+" "+time, "%Y/%m/%d %H:%M")
    debit.transactionDate = transactionDate
    debit.readTransaction = False
    debit.save()

    account.balance = account.balance + amount
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
            prevBudgets = []

            # For budget process
            if credit.subCategoryTransaction != "" and credit.subCategoryTransaction is not None:
                prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=credit.accountNameTransaction_id,
                                    subCategoryBudget_id=credit.subCategoryTransaction_id,
                                    startDate__lte=credit.transactionDate,
                                    endDate__gte=credit.transactionDate)
            elif credit.categoryTransaction_id != "" and credit.categoryTransaction_id is not None:
                prevBudgets = Budget.objects.filter(userBudget_id=request.user,
                                    accountNameBudget_id=credit.accountNameTransaction_id,
                                    categoryBudget_id=credit.categoryTransaction_id,
                                    subCategoryBudget__isnull=True,
                                    startDate__lte=credit.transactionDate,
                                    endDate__gte=credit.transactionDate)
                    
            for budget in prevBudgets:
                currentAmount = budget.currentAmount - credit.amount

                if currentAmount <= 0:
                    currentAmount = 0

                budget.currentAmount = currentAmount

                diff = int(budget.budgetAmount) - int(budget.currentAmount)

                if diff < 0:
                    budget.minusAmount = True
                else:
                    budget.minusAmount = False
                budget.save()

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
        if balance != "" and accounts.balance != int(balance):
            accounts.read = False
        accounts.accountName = request.POST["accountName"]
        accounts.description = request.POST["description"]
        accounts.previousBalance = accounts.balance
        
        if balance == "":
            balance = accounts.balance

        accounts.balance = balance
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

def budget(request):
    
    # Function for automatic update for outdated budgets 
    budgets = Budget.objects.filter(userBudget=request.user)
    currentDate = datetime.now()

    for budget in budgets:
        
        endDate = budget.endDate.replace(tzinfo=None)

        if endDate < currentDate:
            dates = dateSetter(budget.startDate , budget.periodCount , str(budget.periodProcess) )

            dateEnd = dates[1]
            budget.descriptionBudget = countdown(dateEnd)
            dateStart = datetime.strftime(dates[0], "%Y-%m-%d %H:%M")
            dateEnd = datetime.strftime(dateEnd, "%Y-%m-%d %H:%M")


            if budget.subCategoryBudget_id != ""  and budget.subCategoryBudget_id is not None:
                amountData = Transaction.objects.filter(userTransaction=request.user,
                                                accountNameTransaction_id=budget.accountNameBudget_id,
                                                subCategoryTransaction_id=budget.subCategoryBudget_id,
                                                transactionDate__range=[dateStart,dateEnd])
            elif budget.categoryBudget_id != ""  and budget.categoryBudget_id is not None:
                amountData = Transaction.objects.filter(userTransaction=request.user,
                                                accountNameTransaction_id=budget.accountNameBudget_id,
                                                categoryTransaction_id=budget.categoryBudget_id,
                                                subCategoryTransaction__isnull=True,
                                                transactionDate__range=[dateStart,dateEnd])

            amount = 0
            for data in amountData:
                if data.transactionType == "credit":
                    amount += int(data.amount)

            budget.startDate = dateStart
            budget.endDate = dateEnd
            budget.currentAmount = amount

            diff = int(budget.budgetAmount) - amount
            if diff < 0:
                budget.minusAmount = True
            else:
                budget.minusAmount = False

            budget.save()

    return render(request, "budgetApp/budget.html")

def budgetDisplay(request):

    budgets = Budget.objects.filter(userBudget=request.user)
    
    for budget in budgets:
        budget.currentAmount = currencyFormatter(budget.currentAmount)
        budget.budgetAmount = currencyFormatter(budget.budgetAmount)
    
    return JsonResponse([budget.serialize() for budget in budgets], safe=False)

# Add budget screen display
def addBudget(request):

    # Dropdown account, categories and subcategories data
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")
    counts = []
    for count in range(1,32):
        counts.append(count)

    process = []
    process.append({"id": 1, "name":"day(s)"})
    process.append({"id": 2, "name":"week(s)"})
    process.append({"id": 3, "name":"month(s)"})
    process.append({"id": 4, "name":"year(s)"})

    return render(request, "budgetApp/addBudget.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories,
        "counts": counts,
        "process": process,
        "date": datetime.now().strftime("%Y/%m/%d"),
        "time": "0:00"
    })

# Add budget
@csrf_exempt
@login_required
def budgetAdd(request):
    
    data = json.loads(request.body)
    messageList = []
    name = data.get("name")
    amount = data.get("amount")
    description = data.get("description")

    # Name
    if name is not None and len(name) > 25:
        messageList.append({"id":"name", "message":"Please input name within 25 letters."})

    # Amount
    if amount == "":
        messageList.append({"id":"amount", "message":"Please input amount."})

    if amount.find(".") > 0 or amount.find("-") > 0:
        messageList.append({"id":"amount", "message":"Please input integer number."})
    
    if amount is not None and len(amount) > 15:
        messageList.append({"id":"amount", "message":"Please input amount within 15 numbers."})

    # Category and Subcategory
    category = data.get("category")
    subCategory = data.get("subcategory")
    parentSubCategory = ""
    parentExists = True

    if category == "" :
        messageList.append({"id":"category", "message":"Please select category"})

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

    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    budget = Budget()
    budget.userBudget = request.user
    budget.budgetName = data["name"]
    budget.accountNameBudget_id = data["accountName"]
    budget.budgetAmount = data["amount"]
    
    time = data["time"]
    periodCount = int(data["periodCount"])
    periodProcess = data["periodProcess"]
    startDate = datetime.strptime(data["date"]+" "+time, "%Y/%m/%d %H:%M")

    dates = dateSetter(startDate , periodCount , periodProcess)

    dateEnd = dates[1]
    budget.descriptionBudget = countdown(dateEnd)
    dateStart = datetime.strftime(dates[0], "%Y-%m-%d %H:%M")
    dateEnd = datetime.strftime(dateEnd, "%Y-%m-%d %H:%M")

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        budget.categoryBudget_id = category[0]
        budget.subCategoryBudget_id = category[1]
        amountData = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=data["accountName"],
                                        subCategoryTransaction_id=category[1],
                                        transactionDate__range=[dateStart,dateEnd])
    else:
        budget.categoryBudget_id = data["category"]
        amountData = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=data["accountName"],
                                        categoryTransaction_id=data["category"],
                                        subCategoryTransaction__isnull=True,
                                        transactionDate__range=[dateStart,dateEnd])
    
    amount = 0
    for data in amountData:
        if data.transactionType == "credit":
            amount += int(data.amount)
            
    budget.startDate = dateStart
    budget.endDate = dateEnd
    budget.currentAmount = amount
    budget.periodCount = periodCount
    budget.periodProcess = periodProcess

    diff = int(budget.budgetAmount) - amount
    if diff < 0:
        budget.minusAmount = True
    else:
        budget.minusAmount = False

    budget.save()

    return JsonResponse({"message": "success"}, status=200)

# Edit budget screen display
def editBudget(request , id):

    # Dropdown account, categories and subcategories data
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")
    budget = Budget.objects.get(userBudget=request.user,id=id)
    date = budget.startDate.strftime("%Y/%m/%d")
    time = budget.startDate.strftime("%H:%M")
    
    counts = []
    for count in range(1,32):
        counts.append(count)

    process = []
    process.append({"id": 1, "name":"day(s)"})
    process.append({"id": 2, "name":"week(s)"})
    process.append({"id": 3, "name":"month(s)"})
    process.append({"id": 4, "name":"year(s)"})

    return render(request, "budgetApp/editBudget.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories,
        "counts": counts,
        "process": process,
        "budget": budget,
        "date": date,
        "time": time
    })

# Edit budget
@csrf_exempt
@login_required
def budgetEdit(request , id ):
    
    data = json.loads(request.body)
    messageList = []
    name = data.get("name")
    amount = data.get("amount")
    description = data.get("description")

    # Name
    if name is not None and len(name) > 25:
        messageList.append({"id":"name", "message":"Please input name within 25 letters."})

    # Amount
    if amount == "":
        messageList.append({"id":"amount", "message":"Please input amount."})

    if amount.find(".") > 0 or amount.find("-") > 0:
        messageList.append({"id":"amount", "message":"Please input integer number."})
    
    if amount is not None and len(amount) > 15:
        messageList.append({"id":"amount", "message":"Please input amount within 15 numbers."})

    # Category and Subcategory
    category = data.get("category")
    subCategory = data.get("subcategory")
    parentSubCategory = ""
    parentExists = True

    if category == "" :
        messageList.append({"id":"category", "message":"Please select category"})
        
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

    if len(messageList) > 0:
        return JsonResponse({"message":"error","error": messageList}, status=400)

    budget = Budget.objects.get(userBudget=request.user,id=id)
    budget.userBudget = request.user
    budget.budgetName = data["name"]
    budget.accountNameBudget_id = data["accountName"]
    budget.budgetAmount = data["amount"]
    
    time = data["time"]
    periodCount = int(data["periodCount"])
    periodProcess = data["periodProcess"]
    startDate = datetime.strptime(data["date"]+" "+time, "%Y/%m/%d %H:%M")

    dates = dateSetter(startDate , periodCount , periodProcess)

    dateEnd = dates[1]
    budget.descriptionBudget = countdown(dateEnd)
    dateStart = datetime.strftime(dates[0], "%Y-%m-%d %H:%M")
    dateEnd = datetime.strftime(dateEnd, "%Y-%m-%d %H:%M")

    if data["subcategory"] != "":
        category = data["subcategory"].split("-")
        budget.categoryBudget_id = category[0]
        budget.subCategoryBudget_id = category[1]
        amountData = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=data["accountName"],
                                        subCategoryTransaction_id=category[1],
                                        transactionDate__range=[dateStart,dateEnd])
    else:
        budget.categoryBudget_id = data["category"]
        amountData = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=data["accountName"],
                                        categoryTransaction_id=data["category"],
                                        subCategoryTransaction__isnull=True,
                                        transactionDate__range=[dateStart,dateEnd])
    
    amount = 0
    for data in amountData:
        if data.transactionType == "credit":
            amount += int(data.amount)
            
    budget.startDate = dateStart
    budget.endDate = dateEnd
    budget.currentAmount = amount
    budget.periodCount = periodCount
    budget.periodProcess = periodProcess

    diff = int(budget.budgetAmount) - amount
    if diff < 0:
        budget.minusAmount = True
    else:
        budget.minusAmount = False

    budget.save()

    return JsonResponse({"message": "success"}, status=200)

# Display report
def report(request):

    return render(request, "budgetApp/report.html")

# Display expenses and income report
def expensesIncome(request):

    # Dropdown account, categories and subcategories data
    accounts = Account.objects.filter(userAccount=request.user).order_by("accountName")
    categories = Categories.objects.filter(userCategory=request.user).order_by("category")
    subCategories = SubCategories.objects.filter(userSubCategory=request.user).order_by("subCategory")
    years = []
    for count in range(1000,5001):
        years.append(count)

    currentDate = datetime.now()

    return render(request, "budgetApp/expensesIncome.html",{
        "accounts" : accounts,
        "categories" : categories,
        "subCategories" : subCategories,
        "years": years,
        "currentYear": currentDate.year,
    })

@csrf_exempt
@login_required
def expensesIncomeDisplay(request):

    data = json.loads(request.body)
    expenses = []
    income = []
    months = []
    year = data.get("year")
    accountName = data.get("accountName")
    category = data.get("category")
    subCategory = data.get("subcategory")


    for month in range(1,13):
        expensesAmount = 0
        incomeAmount = 0

        if subCategory != ""  and subCategory is not None:
            category = subCategory.split("-")
            subCategorySearch = int(category[1])
            transactions = Transaction.objects.filter(userTransaction=request.user,
                                            accountNameTransaction_id=accountName,
                                            subCategoryTransaction_id=subCategorySearch,
                                            transactionDate__year=year,
                                            transactionDate__month=month)
        elif category != ""  and category is not None:
            transactions = Transaction.objects.filter(userTransaction=request.user,
                                            accountNameTransaction_id=accountName,
                                            categoryTransaction_id=category,
                                            transactionDate__year=year,
                                            transactionDate__month=month)
        else:
            transactions = Transaction.objects.filter(userTransaction=request.user,
                                            accountNameTransaction_id=accountName,
                                            transactionDate__year=year,
                                            transactionDate__month=month)
        if len(transactions) > 0:
            months.append(month)

        for tran in transactions:

            if tran.transactionType == "credit":
                expensesAmount = expensesAmount + tran.amount
            elif tran.transactionType == "debit":
                incomeAmount = incomeAmount + tran.amount
        
        expenses.append(expensesAmount)
        income.append(incomeAmount)
    
    return JsonResponse({"expenses": expenses
                        ,"income": income
                        ,"months": months }, status=200)

@csrf_exempt
@login_required
def expensesIncomeDetail(request):

    data = json.loads(request.body)
    expenses = []
    income = []
    month = data.get("month")
    year = data.get("year")
    accountName = data.get("accountName")
    category = data.get("category")
    subCategory = data.get("subcategory")

    if subCategory != ""  and subCategory is not None and subCategory != 'null':
        category = subCategory.split("-")
        subCategorySearch = int(category[1])
        transactions = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=accountName,
                                        subCategoryTransaction_id=subCategorySearch,
                                        transactionDate__year=year,
                                        transactionDate__month=month)
    elif category != ""  and category is not None and category != 'null':
        transactions = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=accountName,
                                        categoryTransaction_id=category,
                                        transactionDate__year=year,
                                        transactionDate__month=month)
    else:
        transactions = Transaction.objects.filter(userTransaction=request.user,
                                        accountNameTransaction_id=accountName,
                                        transactionDate__year=year,
                                        transactionDate__month=month)

    for tran in transactions:
        tran.amount = currencyFormatter(tran.amount)
        tran.previousAccountBalance = currencyFormatter(tran.previousAccountBalance)
        tran.transactionDate = dateFormatter(tran.transactionDate)
    
    return JsonResponse([transaction.serialize() for transaction in transactions], safe=False)

def dateSetter(startDate, count, process):
    startDate = startDate
    endDate = ""
    currentDate = datetime.now()
    checker = True
    value = []

    while checker:
        if process == "1":    # days
            endDate = startDate + timedelta(days=count)

        if process == "2":    # weeks
            count = count * 7
            endDate = startDate + timedelta(days=count)

        if process == "3":    # months
            month = startDate.month - 1 + count
            year = startDate.year + month // 12
            month = month % 12 + 1
            day = min(startDate.day, calendar.monthrange(year,month)[1])
            endDate = datetime(year, month, day,startDate.hour,startDate.minute)

        if process == "4":    # year
            endDate = datetime(startDate.year + count, startDate.month, startDate.day,startDate.hour,startDate.minute)
        
        endDate = endDate.replace(tzinfo=None)
        if endDate < currentDate:
            startDate = endDate
        else:
            checker = False

    value.append(startDate)
    value.append(endDate)
    return value

def countdown(dateEnd):
    remaining = ""
    days = dateEnd - datetime.now()

    if days.days >= 365:
        remaining = "Ends in: " + datetime.strftime(dateEnd, "%B %d, %Y")
    elif days.days >= 21:
        remaining = "Ends in: " + datetime.strftime(dateEnd, "%B %d")
    elif days.days >= 14:
        remaining = "Ends in: 3 weeks"
    elif days.days >= 7:
        remaining = "Ends in: 2 weeks"
    elif days.days == 1 :
        remaining = "Ends in: "+ str(days.days) +" day"
    elif days.days < 7 :
        remaining = "Ends in: "+ str(days.days) +" days"

    return remaining

# Delete Budget
@csrf_exempt
@login_required
def deleteBudget(request):
    
    data = json.loads(request.body)
    try:
        budget = Budget.objects.get(userBudget=request.user,id=data["item"])
        budget.delete()
    except:
        return JsonResponse({"message": "error"}, status=500)

    return JsonResponse({"message": "success"}, status=200)

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
        error = False
        messageList = []
        username = request.POST["username"].replace(' ','')

        # Ensure password matches confirmation
        password = request.POST["password"].replace(' ','')
        confirmation = request.POST["confirmation"].replace(' ','')

        if username == "":
            messageList.append("Please input a username.")
            error = True

        if password == "":
            messageList.append("Please input a password.")
            error = True
        
        if error:
            return render(request, "budgetApp/register.html", {
                "messages": messageList
            })

        if password != confirmation:
            return render(request, "budgetApp/register.html", {
                "messages": {"Passwords must match."}
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.save()

        except IntegrityError:
            return render(request, "budgetApp/register.html", {
                "messages": {"Username already taken."}
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

    if amount.find(".") > 0 or amount.find("-") > 0:
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