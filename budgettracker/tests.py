from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Transaction, Budget, TransactionType
from datetime import date

class BudgetAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        self.salary_category = Category.objects.create(name='Salary', user=self.user)
        self.groceries_category = Category.objects.create(name='Groceries', user=self.user)
        
        today = date.today()
        Transaction.objects.create(amount=30000, date=today, type=TransactionType.INCOME, category=self.salary_category, user=self.user)
        Transaction.objects.create(amount=14000, date=today, type=TransactionType.EXPENSE, category=self.groceries_category, user=self.user)
        
        Budget.objects.create(month=today.month, year=today.year, amount=40000, user=self.user)
        
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass123'}, format='json')
        self.token = response.data['access']
        self.auth_header = f'Bearer {self.token}'

    def test_budget_status_custom_month_year(self):
        today = date.today()
        response = self.client.get(
            f'/api/budgets/status/?month={today.month}&year={today.year}',
            HTTP_AUTHORIZATION=self.auth_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['month and year'], f"{today.month}/{today.year}")
        self.assertIn('budget_amount', response.data)
        self.assertIn('income_total', response.data)
        self.assertIn('expense_total', response.data)
        self.assertIn('net_savings', response.data)
        self.assertIn('remaining_budget', response.data)

    def test_auth_required(self):
        today = date.today()
        response = self.client.get(f'/api/budgets/status/?month={today.month}&year={today.year}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
