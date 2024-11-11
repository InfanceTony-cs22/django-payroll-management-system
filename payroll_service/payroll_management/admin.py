from django.contrib import admin
from .models import Payroll

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'paid_date', 'net_salary')  # Fields to display in the list view
    search_fields = ('employee__username',)  # Make employee usernames searchable
    list_filter = ('paid_date',)  # Add filters for the paid date
    ordering = ('-paid_date',)  # Order by most recent payrolls first

admin.site.register(Payroll, PayrollAdmin)
