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
    accountNameTransaction = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="accountNameTransaction")
    accountNameTransferFrom = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, related_name="accountNameTransferFrom")
    accountNameTransferTo = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True, related_name="accountNameTransferTo")
    transactionFromId = models.IntegerField(blank=True, null=True)
    transactionType = models.TextField(blank=True)
    amount = models.IntegerField()
    previousAccountBalance = models.IntegerField()
    descriptionTransaction = models.TextField(blank=True)
    categoryTransaction = models.ForeignKey(Categories, on_delete=models.PROTECT, blank=True, null=True, related_name="categoryTransaction")
    subCategoryTransaction = models.ForeignKey(SubCategories, on_delete=models.PROTECT, blank=True, null=True, related_name="subCategoryTransaction")
    transactionDate = models.DateTimeField(auto_now_add=False, blank=True)
    readTransaction = models.BooleanField(default=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userTransaction": self.userTransaction,
            "accountNameTransaction": self.accountNameTransaction,
            "accountNameTransferFrom": self.accountNameTransferFrom,
            "accountNameTransferTo": self.accountNameTransferTo,
            "transactionFromId": self.transactionFromId,
            "transactionType": self.transactionType,
            "amount": self.amount,
            "previousAccountBalance": self.previousAccountBalance,
            "descriptionTransaction": self.descriptionTransaction,
            "categoryTransaction": self.categoryTransaction,
            "subCategoryTransaction": self.subCategoryTransaction,
            "transactionDate": self.transactionDate.strftime("%Y-%m-%d %H:%M:%S"),
            "readTransaction": self.readTransaction,
            "ins_date": self.date.strftime("%Y-%m-%d %H:%M:%S")
        }