from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import User, LoanFund, Loan, AmortizationSchedule
from .serializers import UserSerializer, LoanFundSerializer, LoanSerializer, AmortizationScheduleSerializer
import math


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanFundViewSet(viewsets.ModelViewSet):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def amortization_table(self, request, pk=None):
        loan = get_object_or_404(Loan, pk=pk)
        amortization_schedule = AmortizationSchedule.objects.filter(loan=loan)
        serializer = AmortizationScheduleSerializer(amortization_schedule, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        loan = Loan.objects.get(pk=response.data['id'])
        self.calculate_amortization_schedule(loan)
        return response

    def calculate_amortization_schedule(self, loan):
        principal = float(loan.amount)
        interest_rate = loan.loan_fund.interest_rate / 100 / 12  
        term_months = loan.term

        if interest_rate > 0:
            monthly_payment = principal * (interest_rate * math.pow(1 + interest_rate, term_months)) / (math.pow(1 + interest_rate, term_months) - 1)
        else:
            monthly_payment = principal / term_months

        remaining_balance = principal

        for month in range(1, term_months + 1):
            interest_payment = remaining_balance * interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

            AmortizationSchedule.objects.create(
                loan=loan,
                payment_number=month,
                principal_payment=round(principal_payment, 2),
                interest_payment=round(interest_payment, 2),
                remaining_balance=round(remaining_balance, 2)
            )


class AmortizationScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AmortizationSchedule.objects.all()
    serializer_class = AmortizationScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
