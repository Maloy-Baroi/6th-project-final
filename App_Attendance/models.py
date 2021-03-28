from django.db import models
from App_Login.models import *


# Create your models here.
class Attendance(models.Model):
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    Student_ID = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='attendance_dept')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='attendance_course')
    batch = models.ForeignKey(Batch, on_delete=models.DO_NOTHING, related_name='attendance_batch')
    section = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date) + "_" + str(self.course))
