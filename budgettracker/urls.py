from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BudgetViewSet, TransactionViewSet, Register, Login, TransactionForm, BudgetForm

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('transactionform/', TransactionForm.as_view(), name='transactionform'),
    path('budgetform/', BudgetForm.as_view(), name='budgetform'), 
    
]