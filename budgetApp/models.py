from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.TextField(blank=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "category": self.category,
            "ins_date": self.date.strftime("%b %d %Y, %I:%M %p")
        }

class SubCategories(models.Model):
    parentCategory = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, null=True, related_name="parentCategory")
    subCategory = models.TextField(blank=False)
    ins_date = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "parent Category" : self.parentCategory.category,
            "category": self.category,
            "ins_date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
