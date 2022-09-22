from django.urls import path
from .views import *

urlpatterns = [
    path('user/', get_user),
    path('login/', login),
    path('register/', register),
    path('check_in/',check_in_api,name='checkIn'),
    path('check_out/',check_out_api,name='checkOut'),
    path('attendance_list/',list_check_in,name='attendanceList'),

]