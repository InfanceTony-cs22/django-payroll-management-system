# leave_management/models.py

from django.db import models
from user_management.models import CustomUser  # Import your custom user model

class LeaveRequest(models.Model):
    # Define your fields here
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=50, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], 
        default='Pending'  # Default status is 'Pending'
    )

    # Custom validation for date range (start_date should not be after end_date)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

    class Meta:
        app_label = 'leave_management'  # Explicitly set the app label

    def __str__(self):
        return f"Leave request from {self.employee} for {self.leave_type} leave"
