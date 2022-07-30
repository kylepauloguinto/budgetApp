from django.contrib import admin

from .models import User, Categories, SubCategories

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "ins_date")

class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "parentCategory", "subCategory" ,"ins_date" )

admin.site.register(User)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(SubCategories, SubCategoriesAdmin)