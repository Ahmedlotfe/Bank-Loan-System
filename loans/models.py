from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('bank_personnel', 'Bank Personnel'),
        ('loan_provider', 'Loan Provider'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    groups = models.ManyToManyField(Group, related_name="loans_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="loans_user_permissions", blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class LoanFund(models.Model):
    name = models.CharField(max_length=255)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.FloatField()
    duration = models.IntegerField(help_text="Duration in months") 
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'bank_personnel'}
    )

    def __str__(self):
        return f"{self.name} - {self.min_amount} to {self.max_amount} EGP"


class Loan(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'customer'}
    )
    loan_fund = models.ForeignKey(LoanFund, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField(help_text="Term in months")  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} - {self.amount} EGP by {self.customer.username}"


class AmortizationSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='amortization_schedule')
    payment_number = models.PositiveIntegerField()
    principal_payment = models.DecimalField(max_digits=10, decimal_places=2)
    interest_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.payment_number} - Loan {self.loan.id}"
