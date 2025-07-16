from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BudgetViewSet, TransactionViewSet, RegisterView, LoginView, TransactionFormView, BudgetFormView

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('transactionform/', TransactionFormView.as_view(), name='transactionform'),
    path('budgetform/', BudgetFormView.as_view(), name='budgetform'), 
    
]