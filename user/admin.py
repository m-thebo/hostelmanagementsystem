from django.contrib import admin

from user.models import Student,User,Admin

# Register your models here.
admin.site.register(Student)
admin.site.register(User)
admin.site.register(Admin)