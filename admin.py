from django.contrib import admin
from .models import RegisteredUser , BloodBank ,Ambulance, Appointments , Requests , AnnouncementStaff , MessageUser , AddStaffRequest

# # Register your models here.
admin.site.register(RegisteredUser)
admin.site.register(BloodBank)
admin.site.register(Ambulance)
admin.site.register(Appointments)
admin.site.register(Requests)
admin.site.register(AnnouncementStaff)
admin.site.register(MessageUser)
admin.site.register(AddStaffRequest)