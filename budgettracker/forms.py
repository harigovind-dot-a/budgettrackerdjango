from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Transaction, Budget, Category
import calendar

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TransactionModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter amount'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Optional description...',
                'rows': 3
            }),
        }

class BudgetModelForm(forms.ModelForm):

    month = forms.ChoiceField(
        choices=[(i, calendar.month_name[i]) for i in range(1,13)]
    )
    class Meta:
        model = Budget
        exclude = ['user']
        widgets = {
            'year': forms.NumberInput(attrs={
                'placeholder': 'e.g. 2025'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter budget amount'
            }),
        }   

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Food, Travel, Rent, Salary',
            }),
        }

class BudgetSummaryForm(forms.Form):
    month = forms.ChoiceField(
        choices=[(i, calendar.month_name[i]) for i in range(1, 13)]
    )
    year = forms.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2200)],
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 2025'
        })
    )
