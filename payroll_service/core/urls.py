from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/<int:employee_id>/leave/', views.leave_request, name='leave_request'),
    path('employee/<int:employee_id>/payroll/', views.payroll, name='payroll'),
    path('leave/request/success/', views.leave_request_success, name='leave_request_success'),
    path('payroll/success/', views.payroll_success, name='payroll_success'),
    path('leave/request/success/', views.leave_request_success, name='leave_request_success'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('view_employees/', views.view_employees, name='view_employees'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]
