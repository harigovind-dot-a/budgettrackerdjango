from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BudgetViewSet, TransactionViewSet, CategoryViewSet, BudgetStatusView

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('budget-status/', BudgetStatusView.as_view(), name='budget-status'),
    
]