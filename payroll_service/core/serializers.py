from rest_framework import serializers
from django.contrib.auth.models import User  # Import the User model
from .models import Employee, Leave
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializer for Employee model
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'job_title', 'salary']  # Add fields from your Employee model

# Serializer for Leave model
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'status']  # Adjust according to your Leave model

# User Registration Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
