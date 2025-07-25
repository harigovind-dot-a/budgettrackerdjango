from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from .models import Budget, Transaction, Category, TransactionType
from .forms import RegisterForm, CategoryModelForm, TransactionModelForm, BudgetModelForm, BudgetSummaryForm, AnalyticsForm
from .serializers import BudgetSerializer, TransactionSerializer
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
import calendar

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
        query = getattr(request, "query_params", request.GET)
        month  = int(query.get('month'))
        year = int(query.get('year'))
        budget_obj = (Budget.objects.get(user=user, month=month, year=year))
        if not budget_obj:
            raise ObjectDoesNotExist("No Budget set for this month")
        else:
            budget = budget_obj.amount
        income_total = Transaction.objects.filter(
            user=user,
            type=TransactionType.INCOME,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

        expense_total = Transaction.objects.filter(
            user=user,
            type=TransactionType.EXPENSE,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

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

class Register(FormView):
    template_name = 'budgettracker/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'budgettracker/dashboard.html'

class Login(LoginView):
    template_name = 'budgettracker/login.html'
    success_url = reverse_lazy('dashboard')

class TransactionForm(LoginRequiredMixin, FormView):
    template_name = 'budgettracker/transactionform.html'
    form_class = TransactionModelForm
    success_url = reverse_lazy('list-transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class BudgetForm(LoginRequiredMixin, FormView):
    template_name = 'budgettracker/budgetform.html'
    form_class = BudgetModelForm
    success_url = reverse_lazy('list-budget')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = list(enumerate(calendar.month_name))[1:]
        return context
    
    def form_valid(self, form):
        budget = form.save(commit=False)
        budget.user = self.request.user
        budget.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form)) 

class CategoryForm(LoginRequiredMixin, FormView):
    template_name = 'budgettracker/categoryform.html'
    form_class = CategoryModelForm
    success_url = reverse_lazy('list-category')

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))   

class ListCategoryView(LoginRequiredMixin, TemplateView):
    template_name = 'budgettracker/listcategory.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user).order_by('name')
        return context
    
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'budgettracker/categoryform.html'
    success_url = reverse_lazy('list-category')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('list-category')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class ListTransactionView(LoginRequiredMixin, TemplateView):
    template_name = 'budgettracker/listtransaction.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(user=self.request.user).order_by('-date')
        return context
    
class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'budgettracker/transactionform.html'
    success_url = reverse_lazy('list-transaction')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('list-transaction')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class ListBudgetView(LoginRequiredMixin, TemplateView):
    template_name = 'budgettracker/listbudget.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budgets'] = Budget.objects.filter(user=self.request.user).order_by('-year', '-month')
        return context
    
class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetModelForm
    template_name = 'budgettracker/budgetform.html'
    success_url = reverse_lazy('list-budget')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('list-budget')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetSummaryView(LoginRequiredMixin, FormView):
    template_name = 'budgettracker/summary.html'
    form_class = BudgetSummaryForm

    def form_valid(self, form):
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        context = self.get_context_data(form=form)

        req = APIRequestFactory().get('/api/budgets/status/', {'month': month, 'year': year})
        req.user = self.request.user
        try:
            BudgetViewSet().request = req
            response = BudgetViewSet().budget_status(req)
            context['summary'] = response.data
        except ObjectDoesNotExist as e:
            context['error'] = "No budget set for this month/year"
        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class AnalyticsView(LoginRequiredMixin, FormView):
    template_name = 'budgettracker/chart.html'
    form_class = AnalyticsForm

    def form_valid(self, form):
        month = form.cleaned_data['month']
        year = form.cleaned_data['year']
        tnx_type = form.cleaned_data['type']

        transactions = Transaction.objects.filter(
            user=self.request.user,
            type=tnx_type,
            date__month=month,
            date__year=year
        ).values('category__name').annotate(total=Sum('amount')).order_by('-total')

        labels = [t['category__name'] for t in transactions]
        data = [float(t['total']) for t in transactions]

        context = self.get_context_data(form=form)
        if not labels:
            context['error'] = "No transactions found for the selected month/type."
        else:
            context.update({'labels' : labels, 'data' : data, 'type' : tnx_type})
        return self.render_to_response(context)
