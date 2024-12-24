from django import forms 
from .models import Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["account", "category", "money", "date"]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        
