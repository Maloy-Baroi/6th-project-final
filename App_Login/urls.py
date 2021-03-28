from django.urls import path
from App_Login.views import *

app_name = 'App_Login'

urlpatterns = [
    path('signup/', signup_system, name='signup'),
    path('faculty-signup/', faculty_signup, name='faculty-signup'),
    path('login/', login_system, name='login'),
    path('logout/', logout_system, name='logout'),
]
