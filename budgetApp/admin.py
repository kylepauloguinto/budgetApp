from django.contrib import admin

from .models import User, Categories, SubCategories, Account, Transaction, Budget, Schedule

class AccountAdmin(admin.ModelAdmin):
    list_display = ("id","userAccount", "accountName", "description","balance","previousBalance","read","ins_date")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id","userCategory", "category", "ins_date")

class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ("id","userSubCategory", "parentCategory", "subCategory" ,"ins_date" )
    
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id","userTransaction", "accountNameTransaction", "accountNameTransferFrom", "accountNameTransferTo", "transactionFromId", "transactionType", "amount","previousAccountBalance","currentAccountBalance","descriptionTransaction","scheduleId","categoryTransaction", "subCategoryTransaction", "transactionDate", "readTransaction","ins_date")

class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id","userBudget", "budgetName", "accountNameBudget", "currentAmount", "budgetAmount", "descriptionBudget", "categoryBudget","subCategoryBudget","startDate","endDate", "periodCount", "periodProcess", "minusAmount","ins_date")

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id","userSchedule", "accountNameSchedule", "accountNameScheduleTransferFrom", "accountNameScheduleTransferTo", "scheduleFromId", "scheduleType", "amount","previousScheduleAccountBalance","currentScheduleAccountBalance","descriptionSchedule", "transactionId", "categorySchedule", "subCategorySchedule", "scheduleDate","repeatSchedule","ins_date")

admin.site.register(User)
admin.site.register(Account, AccountAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(SubCategories, SubCategoriesAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Schedule, ScheduleAdmin)