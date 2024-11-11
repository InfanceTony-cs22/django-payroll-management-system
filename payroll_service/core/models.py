from django.db import models

# Employee model
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()
    department = models.CharField(max_length=100, default='HR')  # Default to HR
    job_title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Monthly salary

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def calculate_annual_salary(self):
        """ Calculate the annual salary from monthly salary """
        return self.salary * 12


# Leave model
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)  # e.g., vacation, sick leave
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('pending', 'Pending')])

    def __str__(self):
        return f'{self.leave_type} leave for {self.employee} from {self.start_date} to {self.end_date}'

    def get_leave_duration(self):
        """ Calculate the number of days of leave taken """
        return (self.end_date - self.start_date).days


# Payroll model
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Monthly salary
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Deductions (taxes, etc.)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Calculated net salary
    month = models.CharField(max_length=20)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.employee} payroll for {self.month}/{self.year}'

    def calculate_net_salary(self):
        """ Calculate net salary by subtracting deductions from salary """
        self.net_salary = self.salary - self.deductions
        self.save()  # Save the calculated net salary to the model
        return self.net_salary
