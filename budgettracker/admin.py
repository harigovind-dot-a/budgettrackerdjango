from django.contrib import admin

# Register your models here.
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'user', 'type')
    list_filter = ('category', 'date', 'user', 'type')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'amount', 'user')
    list_filter = ('month', 'year', 'user')
