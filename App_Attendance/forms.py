from django import forms

from App_Attendance.models import Attendance
from App_Login.models import Faculty


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['department', 'course', 'batch', 'section']

