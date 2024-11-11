from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_management.views import UserViewSet
from core.views import EmployeeViewSet
from leave_management.views import LeaveRequestViewSet
from payroll_management.views import PayrollViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)
router.register(r'payroll', PayrollViewSet)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_management/', include('user_management.urls')),
    path('payroll_management/', include('payroll_management.urls')),
    path('leave_management/', include('leave_management.urls')),
    path('', include('core.urls')),  # Include the core app's URLs
    path('api/', include(router.urls)),
]
