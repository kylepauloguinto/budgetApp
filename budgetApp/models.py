from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Account(models.Model):
    userAccount = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAccount")
    accountName = models.TextField(blank=False)
    description = models.TextField(blank=True)
    balance = models.IntegerField()
    previousBalance = models.IntegerField()
    read = models.BooleanField(default=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userAccount": self.userAccount,
            "accountName": self.accountName,
            "description": self.description,
            "balance" : self.balance,
            "previousBalance" : self.previousBalance,
            "read" : self.read,
            "ins_date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self):
        return f"{self.accountName}"

class Categories(models.Model):
    userCategory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCategory")
    category = models.TextField(blank=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userCategory": self.userCategory,
            "category": self.category,
            "ins_date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self):
        return f"{self.category}"

class SubCategories(models.Model):
    userSubCategory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userSubCategory")
    parentCategory = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="parentCategory")
    subCategory = models.TextField(blank=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userSubCategory": self.userSubCategory,
            "parent Category" : self.parentCategory.category,
            "category": self.category,
            "ins_date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"{self.subCategory}"

class Transaction(models.Model):
    userTransaction = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userTransaction")
    accountNameTransaction = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="accountNameTransaction")
    accountNameTransferFrom = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="accountNameTransferFrom")
    accountNameTransferTo = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="accountNameTransferTo")
    transactionFromId = models.IntegerField(blank=True, null=True)
    transactionType = models.TextField(blank=True)
    amount = models.IntegerField()
    previousAccountBalance = models.IntegerField()
    currentAccountBalance = models.IntegerField()
    descriptionTransaction = models.TextField(blank=True)
    scheduleId = models.IntegerField(blank=True, null=True)
    categoryTransaction = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="categoryTransaction")
    subCategoryTransaction = models.ForeignKey(SubCategories, on_delete=models.CASCADE, blank=True, null=True, related_name="subCategoryTransaction")
    transactionDate = models.DateTimeField(auto_now_add=False, blank=True)
    readTransaction = models.BooleanField(default=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "accountNameTransaction": self.accountNameTransaction.accountName,
            "accountNameTransferFrom": "" if self.accountNameTransferFrom == None else self.accountNameTransferFrom.accountName,
            "accountNameTransferFromId": "" if self.accountNameTransferFrom == None else self.accountNameTransferFrom.id,
            "accountNameTransferTo": "" if self.accountNameTransferTo == None else self.accountNameTransferTo.accountName,
            "accountNameTransferToId": "" if self.accountNameTransferTo == None else self.accountNameTransferTo.id,
            "transactionFromId": self.transactionFromId,
            "transactionType": self.transactionType,
            "amount": self.amount,
            "previousAccountBalance": self.previousAccountBalance,
            "descriptionTransaction": self.descriptionTransaction,
            "transactionDate": self.transactionDate,
            "readTransaction": self.readTransaction
        }

class Budget(models.Model):
    userBudget = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBudget")
    budgetName = models.TextField(blank=False)
    accountNameBudget = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="accountNameBudget")
    currentAmount = models.IntegerField()
    budgetAmount = models.IntegerField()
    descriptionBudget = models.TextField(blank=True)
    categoryBudget = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="categoryBudget")
    subCategoryBudget = models.ForeignKey(SubCategories, on_delete=models.CASCADE, blank=True, null=True, related_name="subCategoryBudget")
    startDate = models.DateTimeField(auto_now_add=False, blank=True)
    endDate = models.DateTimeField(auto_now_add=False, blank=True)
    periodCount = models.IntegerField()
    periodProcess = models.IntegerField()
    minusAmount = models.BooleanField(default=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "budgetName": self.budgetName,
            "accountNameBudget": self.accountNameBudget.accountName,
            "currentAmount": self.currentAmount,
            "budgetAmount": self.budgetAmount,
            "descriptionBudget": self.descriptionBudget,
            "minusAmount": self.minusAmount,
            "ins_date": self.ins_date
        }

class Schedule(models.Model):
    userSchedule = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userSchedule")
    accountNameSchedule = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="accountNameSchedule")
    accountNameScheduleTransferFrom = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="accountNameScheduleTransferFrom")
    accountNameScheduleTransferTo = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="accountNameScheduleTransferTo")
    scheduleFromId = models.IntegerField(blank=True, null=True)
    scheduleType = models.TextField(blank=True)
    amount = models.IntegerField()
    previousScheduleAccountBalance = models.IntegerField()
    currentScheduleAccountBalance = models.IntegerField()
    descriptionSchedule = models.TextField(blank=True)
    transactionId = models.IntegerField(blank=True, null=True)
    categorySchedule = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="categorySchedule")
    subCategorySchedule = models.ForeignKey(SubCategories, on_delete=models.CASCADE, blank=True, null=True, related_name="subCategorySchedule")
    startScheduleDate = models.DateTimeField(auto_now_add=False, blank=True)
    nextScheduleDate = models.DateTimeField(auto_now_add=False, blank=True)
    nextScheduleDateText = models.TextField(blank=True)
    endScheduleDate = models.DateTimeField(auto_now_add=False, blank=True)
    endedSchedule = models.BooleanField(default=False)
    neverEndSchedule = models.BooleanField(default=False)
    repeatSchedule = models.BooleanField(default=False)
    periodCountSchedule = models.IntegerField(blank=True, null=True)
    periodProcessSchedule = models.IntegerField(blank=True, null=True)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "accountNameSchedule": self.accountNameSchedule.accountName,
            "accountNameScheduleTransferFrom": "" if self.accountNameScheduleTransferFrom == None else self.accountNameScheduleTransferFrom.accountName,
            "accountNameScheduleTransferFromId": "" if self.accountNameScheduleTransferFrom == None else self.accountNameScheduleTransferFrom.id,
            "accountNameScheduleTransferTo": "" if self.accountNameScheduleTransferTo == None else self.accountNameScheduleTransferTo.accountName,
            "accountNameScheduleTransferToId": "" if self.accountNameScheduleTransferTo == None else self.accountNameScheduleTransferTo.id,
            "scheduleFromId": self.scheduleFromId,
            "scheduleType": self.scheduleType,
            "amount": self.amount,
            "descriptionSchedule": self.descriptionSchedule,
            "startScheduleDate": self.startScheduleDate,
            "nextScheduleDateText": self.nextScheduleDateText,
            "repeatSchedule": self.repeatSchedule
        }

class Report(models.Model):
    userReport = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userReport")
    startDate = models.DateTimeField(auto_now_add=False, blank=True)
    accountNameReport = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="accountNameReport")
    amount = models.IntegerField()
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "startDate": self.startDate,
            "accountNameReport": self.accountNameReport.accountName,
            "amount": self.amount,
            "ins_date": self.ins_date
        }