"""
URL configuration for financetracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.urls import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("expense/", views.expense, name="expense"),
    path("income/", views.income, name="income"),
    path("<int:pk>/edit_expense/", views.edit_expense, name="edit_expense"),
    path("<int:pk>/edit_income/", views.edit_income, name="edit_income"),
    path("<int:pk>/delete_expense/", views.delete_expense, name="delete_expense"),
    path("<int:pk>/delete_income/", views.delete_income, name="delete_income"),
    path("info/", views.info, name="info"),
    path("expense_chart/", views.expense_chart, name="expense_chart"),
    path("income_chart/", views.income_chart, name="income_chart"),
    path("budget/", views.budget, name="budget"),
    path("budget_plot/", views.budget_plot, name="budget_plot"),
    path("<int:pk>/edit_budget/", views.edit_budget, name="edit_budget"),
    path("<int:pk>/delete_budget/", views.delete_budget, name="delete_budget"),
    path("register/", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
