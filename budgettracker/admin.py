from django.contrib import admin

# Register your models here.
from .models import Transaction, Budget

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'user')
    list_filter = ('category', 'date', 'user')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'amount', 'user')
    list_filter = ('month', 'year', 'user')
