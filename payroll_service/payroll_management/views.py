# payroll_management/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Payroll
from .serializers import PayrollSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# API ViewSet for Payroll Management
class PayrollPagination(PageNumberPagination):
    page_size = 10  # You can adjust this number based on your needs

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view
    pagination_class = PayrollPagination  # Optional: Add pagination to the API
    
    def perform_create(self, serializer):
        # You can add custom payroll logic here, for example:
        payroll = serializer.save()
        # Optional: Net Salary calculation logic can be added here if needed
        # payroll.net_salary = payroll.salary - payroll.deductions + payroll.bonuses
        # payroll.save()

# Frontend View for Viewing Payroll Data
@login_required
def view_payroll(request):
    # Ensure the user is linked to an employee record
    payrolls = Payroll.objects.filter(employee=request.user.employee)  # Assuming user is linked to Employee model
    return render(request, 'templates/view_payroll.html', {'payrolls': payrolls})

