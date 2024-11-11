from django.contrib import admin
from .models import Employee, Leave, Payroll

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'job_title', 'salary')
    search_fields = ('first_name', 'last_name', 'email', 'department')
    list_filter = ('department', 'job_title')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'leave_type')
    list_filter = ('status', 'leave_type')
    date_hierarchy = 'start_date'

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'deductions', 'net_salary', 'month', 'year')
    search_fields = ('employee__first_name', 'employee__last_name', 'month', 'year')
    list_filter = ('month', 'year')
