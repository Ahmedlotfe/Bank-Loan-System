from rest_framework import serializers
from .models import User, LoanFund, Loan, AmortizationSchedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']


class LoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanFund
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class AmortizationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmortizationSchedule
        fields = '__all__'
