from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Budget, Transaction, CategoryType
from .serializers import BudgetSerializer, TransactionSerializer
from django.db.models import Sum
from django.views.generic import TemplateView

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='status')
    def budget_status(self, request):
        user = request.user
        month  = int(request.query_params['month'])
        year = int(request.query_params['year'])
        budget = (Budget.objects.get(user=user, month=month, year=year)).amount

        income_total = Transaction.objects.filter(
            user=user,
            category=CategoryType.INCOME ,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum']

        expense_total = Transaction.objects.filter(
            user=user,
            category=CategoryType.EXPENSE ,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum']

        net_savings = income_total - expense_total
        remaining_budget = budget - expense_total

        data = {
            'month and year': f"{month}/{year}",
            'budget_amount': budget,
            'income_total': income_total,
            'expense_total': expense_total,
            'net_savings': net_savings,
            'remaining_budget': remaining_budget
        }

        return Response(data)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(TemplateView):
    template_name = 'budgettracker/register.html'

class LoginView(TemplateView):
    template_name = 'budgettracker/login.html'

class TransactionFormView(TemplateView):
    template_name = 'budgettracker/transactionform.html'

class BudgetFormView(TemplateView):
    template_name = 'budgettracker/budgetform.html'