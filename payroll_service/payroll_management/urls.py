# payroll_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayrollViewSet, view_payroll  # Import both the ViewSet and custom view

# Create a router and register the PayrollViewSet
router = DefaultRouter()
router.register(r'payrolls', PayrollViewSet, basename='payroll')

urlpatterns = [
    # Include all the routes automatically generated by the DefaultRouter for CRUD operations on Payroll
    path('', include(router.urls)),
    
    # Custom view for rendering payroll (if required for frontend)
    path('view/', view_payroll, name='view_payroll'),  # Custom view for rendering payroll
]