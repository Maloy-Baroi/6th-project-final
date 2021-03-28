from django.urls import path
from App_Attendance import views

app_name = 'App_Attendance'

urlpatterns = [
    path('', views.index, name='Home'),
    path('attendance/', views.take_attendance, name='Attendance'),
]
