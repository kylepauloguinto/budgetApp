from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Account(models.Model):
    userAccount = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAccount")
    accountName = models.TextField(blank=False)
    description = models.TextField(blank=True)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userAccount": self.userAccount,
            "accountName": self.accountName,
            "description": self.description,
            "ins_date": self.date.strftime("%b %d %Y, %I:%M %p")
        }

class Categories(models.Model):
    userCategory = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userCategory")
    category = models.TextField(blank=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "userCategory": self.userCategory,
            "category": self.category,
            "ins_date": self.date.strftime("%b %d %Y, %I:%M %p")
        }

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
            "ins_date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
