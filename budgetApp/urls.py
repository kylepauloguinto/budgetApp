
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("transaction", views.transaction, name="transaction"),
    
    path("creditAdd", views.creditAdd, name="creditAdd"),
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