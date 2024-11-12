# payroll_management/tasks.py

from celery import shared_task
from .models import Payroll
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def process_payroll():
    payrolls = Payroll.objects.all()
    for payroll in payrolls:
        # Calculate net salary (example logic)
        payroll.net_salary = payroll.gross_salary - 100  # Simple deduction logic
        payroll.save()

        # Send email with payroll info
        send_mail(
            'Your Payroll Information',
            f'Your net salary for this period is {payroll.net_salary}',
            settings.DEFAULT_FROM_EMAIL,
            [payroll.employee.email],
            fail_silently=False,
        )
    return "Payroll processing complete"
