from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty')
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to='Faculty_image', null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.class_id  # + "_" + instance.department + "_" + instance.batch + "_" + instance.section
    filename = name + '.' + ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.department, instance.batch, instance.section, filename)


# Department ++ Section ++ Course
class Department(models.Model):
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.department}"


class Batch(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_in_semester')
    Batch = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.department} {self.Batch}"


class Course(models.Model):
    Batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='semester_in_courses')
    course_code = models.CharField(max_length=255)
    course = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course_code}-{self.course}"


SECTION = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
)
# End


class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    class_id = models.CharField(max_length=200, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_name')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='Batch_name')
    section = models.CharField(max_length=100, null=True, choices=SECTION)
    profile_pic = models.ImageField(upload_to=student_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.class_id)
