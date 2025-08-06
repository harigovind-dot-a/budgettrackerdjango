####################### Used for Django Template, not required for Angular #######################
"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Login, Register, DashboardView, ListBudgetView, ListTransactionView, ListCategoryView, TransactionForm, BudgetForm, CategoryForm, TransactionDeleteView, BudgetDeleteView, CategoryDeleteView, TransactionUpdateView, BudgetUpdateView, CategoryUpdateView, BudgetSummaryView, AnalyticsView


urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register'),

    path('budgets/', ListBudgetView.as_view(), name='list-budget'),
    path('transactions/', ListTransactionView.as_view(), name='list-transaction'),
    path('categories/', ListCategoryView.as_view(), name='list-category'),
    path('summary/', BudgetSummaryView.as_view(), name='budget-summary'),
    path('analytics/', AnalyticsView.as_view(), name='chart'),

    path('transactionform/', TransactionForm.as_view(), name='transactionform'),
    path('budgetform/', BudgetForm.as_view(), name='budgetform'),
    path('categoryform/', CategoryForm.as_view(), name='categoryform'),

    path('transaction/delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete-transaction'),
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='delete-budget'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category'),

    path('transaction/edit/<int:pk>/', TransactionUpdateView.as_view(), name='edit-transaction'),
    path('budget/edit/<int:pk>/', BudgetUpdateView.as_view(), name='edit-budget'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit-category'),

]
"""