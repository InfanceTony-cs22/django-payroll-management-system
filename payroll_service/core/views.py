from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Leave, Payroll
from .forms import LeaveForm, PayrollForm, EmployeeForm  # Import the EmployeeForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployeeSerializer

# View for employee list
def index(request):
    employees = Employee.objects.all()
    return render(request, 'index.html', {'employees': employees})

# View for adding a new employee
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to employee list after adding
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

# View for creating leave requests
def leave_request(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            return redirect('leave_request_success')  # Redirect to success page after leave request
    else:
        form = LeaveForm()
    return render(request, 'leave_request.html', {'form': form, 'employee': employee})

# View for managing payroll
def payroll(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.employee = employee
            payroll.net_salary = payroll.calculate_net_salary()
            payroll.save()
            return redirect('payroll_success')  # Redirect to success page after payroll is processed
    else:
        form = PayrollForm()
    return render(request, 'payroll.html', {'form': form, 'employee': employee})

# Success view for payroll processing
def payroll_success(request):
    return render(request, 'payroll_success.html')  # Render the payroll success page

# Success view for leave request
def leave_request_success(request):
    return render(request, 'leave_request_success.html')  # Render the leave request success page

# Employee API ViewSet for the API section
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]