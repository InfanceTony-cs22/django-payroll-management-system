from django import forms
from .models import Employee, Leave, Payroll

# Form for creating/updating employee details
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'department', 'job_title', 'salary']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'hire_date': 'Hire Date',
            'department': 'Department',
            'job_title': 'Job Title',
            'salary': 'Monthly Salary',
        }
        help_texts = {
            'email': 'Enter a valid email address.',
            'phone_number': 'Enter phone number in the format: +1234567890.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

# Form for creating leave requests
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'leave_type': 'Type of Leave',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        help_texts = {
            'leave_type': 'e.g., Vacation, Sick Leave, etc.',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('End date cannot be earlier than start date.')

        return cleaned_data

# Form for payroll management
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['salary', 'deductions', 'month', 'year']
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'e.g., January'}),
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2100}),
        }
        labels = {
            'salary': 'Monthly Salary',
            'deductions': 'Deductions',
            'month': 'Payroll Month',
            'year': 'Payroll Year',
        }
        help_texts = {
            'salary': 'Enter the monthly salary of the employee.',
            'deductions': 'Enter any deductions for this month.',
        }

    def clean(self):
        cleaned_data = super().clean()
        salary = cleaned_data.get('salary')
        deductions = cleaned_data.get('deductions')

        if deductions and salary and deductions > salary:
            self.add_error('deductions', 'Deductions cannot exceed the salary.')

        if not cleaned_data.get('month').isalpha():
            self.add_error('month', 'Month should be a valid string, e.g., "January".')

        return cleaned_data
