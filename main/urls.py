from django.urls import path
from .views import (
    staff_list, staff_detail, add_staff, edit_staff, delete_staff,
    add_assignment, edit_assignment, delete_assignment,
    pay_money
)

urlpatterns = [
    path('', staff_list, name='staff_list'),
    path('staff/<int:pk>/', staff_detail, name='staff_detail'),
    path('add-staff/', add_staff, name='add_staff'),
    path('edit-staff/<int:pk>/', edit_staff, name='edit_staff'),
    path('delete-staff/<int:pk>/', delete_staff, name='delete_staff'),
    path('staff/<int:staff_id>/add-assignment/', add_assignment, name='add_assignment'),
    path('edit-assignment/<int:pk>/', edit_assignment, name='edit_assignment'),
    path('delete-assignment/<int:pk>/', delete_assignment, name='delete_assignment'),
    path('staff/<int:pk>/pay-money/', pay_money, name='pay_money'),
]