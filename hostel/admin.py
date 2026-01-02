from django.contrib import admin
from hostel.models import *
# Register your models here.

admin.site.register(Hostel)
admin.site.register(Wing)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Complaint)
admin.site.register(Application)