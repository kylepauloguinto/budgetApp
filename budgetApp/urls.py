
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("transaction", views.transaction, name="transaction"),

    path("listCategories",views.listCategories, name="listCategories"),
    path("editCategory/<int:id>",views.editCategory, name="editCategory"),
    path("editSubCategory/<int:id>",views.editSubCategory, name="editSubCategory"),
    path("addCategory",views.addCategory, name="addCategory"),
]