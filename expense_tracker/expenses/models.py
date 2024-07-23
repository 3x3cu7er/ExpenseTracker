from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=100,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ], default='Other')

    def __str__(self):
        return f"{self.title} - {self.amount}"
