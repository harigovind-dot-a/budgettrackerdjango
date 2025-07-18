from django.contrib import admin
from .models import Transaction, Budget, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','category', 'type', 'amount', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('category', 'type', 'date')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'amount', 'user')
    list_filter = ('month', 'year', 'user')
    search_fields = ('month', 'year')
