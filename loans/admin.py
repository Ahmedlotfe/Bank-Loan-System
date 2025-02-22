from django.contrib import admin
from .models import User, LoanFund, Loan, AmortizationSchedule

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'user_type')
    list_filter = ('user_type', 'is_staff', 'is_active')


@admin.register(LoanFund)
class LoanFundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_amount', 'max_amount', 'interest_rate', 'duration', 'created_by')
    search_fields = ('name',)
    list_filter = ('interest_rate', 'duration')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'loan_fund', 'amount', 'term', 'created_at')
    search_fields = ('customer__username', 'loan_fund__name')
    list_filter = ('term', 'created_at')


@admin.register(AmortizationSchedule)
class AmortizationScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'payment_number', 'principal_payment', 'interest_payment', 'remaining_balance')
    search_fields = ('loan__customer__username',)
    list_filter = ('payment_number',)
