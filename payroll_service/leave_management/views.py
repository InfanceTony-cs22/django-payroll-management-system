# leave_management/views.py
from rest_framework import viewsets
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import StandardResultsSetPagination  # Optional pagination

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, updating, and deleting leave requests.
    """
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'status']
    ordering_fields = ['paid_date']
    pagination_class = StandardResultsSetPagination  # Optional pagination

def request_leave(request):
    # Your logic to handle leave requests
    return render(request, 'leave_management/request_leave.html')