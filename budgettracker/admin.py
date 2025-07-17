from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import Transaction, Budget

admin.site.register(CustomUser, UserAdmin)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'user')
    list_filter = ('category', 'date', 'user')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'amount', 'user')
    list_filter = ('month', 'year', 'user')
