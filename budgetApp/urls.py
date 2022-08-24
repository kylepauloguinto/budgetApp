
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    path("display/<int:id>", views.display, name="display"),
    path("display/unread/<int:id>", views.unread, name="unread"),
    path("display/transaction/<int:id>", views.transaction, name="transaction"),

    path("addTransaction", views.addTransaction, name="addTransaction"),
    path("display/editTransaction/<int:id>", views.editTransaction, name="editTransaction"),
    
    path("creditEdit/<int:id>", views.creditEdit, name="creditEdit"),
    path("debitEdit/<int:id>", views.debitEdit, name="debitEdit"),
    path("transferEdit/<int:id>", views.transferEdit, name="transferEdit"),
    path("addTransaction/creditAdd", views.creditAdd, name="creditAdd"),
    path("debitAdd", views.debitAdd, name="debitAdd"),
    path("transferAdd", views.transferAdd, name="transferAdd"),

    path("settings", views.settings, name="settings"),

    path("accounts",views.accounts, name="accounts"),
    path("addAccount",views.addAccount, name="addAccount"),
    path("editAccount/<int:id>",views.editAccount, name="editAccount"),

    path("categories",views.categories, name="categories"),
    path("editCategory/<int:id>",views.editCategory, name="editCategory"),
    path("editSubCategory/<int:id>",views.editSubCategory, name="editSubCategory"),
    path("addCategory",views.addCategory, name="addCategory"),
]