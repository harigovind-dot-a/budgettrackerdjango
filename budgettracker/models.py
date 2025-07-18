from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class TransactionType(models.IntegerChoices):
    INCOME = 1, 'Income'
    EXPENSE = 2, 'Expense'

class Transaction(models.Model):
    type = models.PositiveSmallIntegerField(choices=TransactionType.choices, default=TransactionType.EXPENSE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"
    
    def clean(self):
        if self.category.user != self.user:
            raise ValidationError("Category does not belong to this user.")
        else:
            pass

class Budget(models.Model):
    month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2200)])
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"{self.user.username}'s Budget for {self.month}/{self.year}"
