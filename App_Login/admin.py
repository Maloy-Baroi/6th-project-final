from django.contrib import admin
from App_Login.models import Faculty, Student, Department, Batch, Course

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Batch)
admin.site.register(Course)

