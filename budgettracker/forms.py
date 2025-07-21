from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Budget, Category

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user']

class BudgetModelForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ['user']

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user']
