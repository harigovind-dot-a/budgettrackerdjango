from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    
]