from django.db import models
from user_management.models import CustomUser  # Assuming CustomUser model is in user_management

class Payroll(models.Model):
    # Employee-related fields
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    # Salary fields
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Payroll date and status
    paid_date = models.DateField()
    pay_period_start = models.DateField()  # Start date of the payroll period
    pay_period_end = models.DateField()    # End date of the payroll period
    
    # Optional: Add a status to track payroll processing
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    class Meta:
        app_label = 'payroll_management'  # Explicitly set the app label

    def save(self, *args, **kwargs):
        # Ensure no negative values for salary, deductions, or bonuses
        if self.salary < 0 or self.deductions < 0 or self.bonuses < 0:
            raise ValueError("Salary, deductions, and bonuses cannot be negative.")
        
        # Calculate net salary before saving
        self.net_salary = self.salary - self.deductions + self.bonuses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll for {self.employee.username} - {self.paid_date}"

    # You can add more utility methods if necessary
    def is_payroll_overdue(self):
        # Check if the payroll payment is overdue
        return self.paid_date < models.DateField.today()
