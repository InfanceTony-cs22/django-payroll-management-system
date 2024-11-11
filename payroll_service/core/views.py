from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Leave, Payroll
from .forms import LeaveForm, PayrollForm, EmployeeForm  # Import the EmployeeForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployeeSerializer
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Leave
from .serializers import EmployeeSerializer, LeaveSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



# View for employee list
def index(request):
    employees = Employee.objects.all()
    return render(request, 'index.html', {'employees': employees})

# View for adding a new employee
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to employee list after adding
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

# View for creating leave requests
def leave_request(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.save()
            return redirect('leave_request_success')  # Redirect to success page after leave request
    else:
        form = LeaveForm()
    return render(request, 'leave_request.html', {'form': form, 'employee': employee})

# View for managing payroll
def payroll(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.employee = employee
            payroll.net_salary = payroll.calculate_net_salary()
            payroll.save()
            return redirect('payroll_success')  # Redirect to success page after payroll is processed
    else:
        form = PayrollForm()
    return render(request, 'payroll.html', {'form': form, 'employee': employee})

# Success view for payroll processing
def payroll_success(request):
    return render(request, 'payroll_success.html')  # Render the payroll success page

# Success view for leave request
def leave_request_success(request):
    return render(request, 'leave_request_success.html')  # Render the leave request success page

def view_employees(request):
    # Your logic to fetch and display employees
    employees = Employee.objects.all()  # Replace with actual logic
    return render(request, 'view_employees.html', {'employees': employees})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('view_employees')  # Redirect to the employee list view after deletion
    
    return render(request, 'confirm_delete.html', {'employee': employee})

def view_employees(request):
    employees = Employee.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

def payroll_success(request):
    return render(request, 'payroll_success.html')

# Employee API ViewSet for the API section
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]



# View to handle Employee CRUD
class EmployeeListCreateAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to handle a single Employee (Retrieve, Update, Delete)
class EmployeeDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# View to handle Leave CRUD
class LeaveListCreateAPIView(APIView):
    def get(self, request):
        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to handle a single Leave (Retrieve, Update, Delete)
class LeaveDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveSerializer(leave)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)

        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginUserAPIView(APIView):
    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate the JWT token using SimpleJWT's RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),  # Refresh token
                'access': str(refresh.access_token),  # Access token
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

