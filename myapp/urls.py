"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from budgettracker.views import Login, DashboardView, Register, ListBudgetView, ListCategoryView, ListTransactionView, TransactionForm, BudgetForm, CategoryForm, TransactionDeleteView, BudgetDeleteView, CategoryDeleteView, TransactionUpdateView, BudgetUpdateView, CategoryUpdateView, BudgetSummaryView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Login.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register'),

    path('budgets/', ListBudgetView.as_view(), name='list-budget'),
    path('transactions/', ListTransactionView.as_view(), name='list-transaction'),
    path('categories/', ListCategoryView.as_view(), name='list-category'),
    path('summary/', BudgetSummaryView.as_view(), name='budget-summary'),

    path('transactionform/', TransactionForm.as_view(), name='transactionform'),
    path('budgetform/', BudgetForm.as_view(), name='budgetform'),
    path('categoryform/', CategoryForm.as_view(), name='categoryform'),
    
    path('transaction/delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete-transaction'),
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='delete-budget'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category'),

    path('transaction/edit/<int:pk>/', TransactionUpdateView.as_view(), name='edit-transaction'),
    path('budget/edit/<int:pk>/', BudgetUpdateView.as_view(), name='edit-budget'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit-category'),

    path('api/', include('budgettracker.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
