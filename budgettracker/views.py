from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Budget, Transaction, Category
from .serializers import BudgetSerializer, TransactionSerializer, CategorySerializer
from django.db.models import Sum
from datetime import date

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_budget(self):
        today = date.today()
        qs = self.get_queryset().filter(month=today.month, year=today.year)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = date.today()
        month = today.month
        year = today.year

        budget = Budget.objects.filter(user=user, month=month, year=year).first()
        budget_amount = budget.amount if budget else 0.00

        income_total = Transaction.objects.filter(
            user=user,
            category__type = 1 ,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0.00

        expense_total = Transaction.objects.filter(
            user=user,
            category__type= 2 ,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0.00

        net_savings = income_total - expense_total
        remaining_budget = budget_amount - expense_total

        data = {
            'month and year': f"{month}/{year}",
            'budget_amount': budget_amount,
            'income_total': income_total,
            'expense_total': expense_total,
            'net_savings': net_savings,
            'remaining_budget': remaining_budget
        }

        return Response(data)
