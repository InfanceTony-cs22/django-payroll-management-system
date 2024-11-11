from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet  # Make sure this matches the existing view in views.py

router = DefaultRouter()
router.register(r'users', UserViewSet)  # Register UserViewSet, not CustomUserViewSet

urlpatterns = [
    path('', include(router.urls)),
]
