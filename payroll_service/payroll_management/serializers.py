# payroll_management/serializers.py
from rest_framework import serializers
from .models import Payroll

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ['id', 'employee', 'salary', 'paid_date', 'deductions', 'bonuses', 'net_salary']
