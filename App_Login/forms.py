from django.contrib.auth.forms import UserCreationForm
from django import forms
from App_Login.models import *


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class CreateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user']


