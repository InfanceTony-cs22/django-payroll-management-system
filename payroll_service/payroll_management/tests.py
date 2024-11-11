# payroll_management/tests.py
from django.test import TestCase
from .models import Payroll
from user_management.models import CustomUser  # Adjust according to your CustomUser location

class PayrollTestCase(TestCase):
    def setUp(self):
        # Create a user instance
        self.user = CustomUser.objects.create_user(username="john_doe", password="password123")
        # Create a payroll instance
        self.payroll = Payroll.objects.create(
            employee=self.user,
            salary=5000,
            paid_date="2024-11-01",
            deductions=500,
            bonuses=200
        )

    def test_net_salary_calculation(self):
        # Verify the net salary calculation
        self.assertEqual(self.payroll.net_salary, 4700)
    
    def test_str_method(self):
        # Verify the string representation
        self.assertEqual(str(self.payroll), "Payroll for john_doe - 2024-11-01")
