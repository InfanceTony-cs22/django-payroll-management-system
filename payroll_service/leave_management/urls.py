# leave_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet
from django.urls import path
from . import views

# Create a router and register your viewset
router = DefaultRouter()
router.register(r'leave_requests', LeaveRequestViewSet, basename='leave-request')

# Include the router URLs
urlpatterns = [
    path('', include(router.urls)),
    path('request/', views.request_leave, name='request_leave'),
    
    
]
