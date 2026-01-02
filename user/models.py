from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    semester = models.IntegerField()
    application_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " | " + self.student_id

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    admin_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

