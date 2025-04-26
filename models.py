from django.db import models
from django_mysql.models import ListCharField

class RegisteredUser(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    user_username = models.CharField(max_length=500,default=' ')
    name = models.CharField(max_length=200,default=' ')
    email = models.EmailField(default=' ')
    mobile = models.CharField(max_length=15,default=' ')
    age = models.CharField(max_length=100,default=' ')
    address = models.CharField(max_length=500,default=' ')
    def __str__(self):
        return self.name

class BloodBank(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    name = models.CharField(max_length=500,default=' ')
    address = models.CharField(max_length=500,default=' ')
    state = models.CharField(max_length=100,default=' ')
    city = models.CharField(max_length=100,default=' ')
    mobile = models.CharField(max_length=100,default=' ')
    email = models.EmailField(default=' ')
    category = models.CharField(max_length=100,default=' ')
    status = models.CharField(max_length=100,default=' ')
    website = models.CharField(max_length=800,default=' ')
    blood_groups =  ListCharField(
        base_field=models.CharField(max_length=5),
        size=10,
        max_length=(10 * 10)  # 6 * 10 character nominals, plus commas,
    )
    A_positive_units = models.CharField(max_length=10, default='')
    A_negative_units = models.CharField(max_length=10, default='')
    B_positive_units = models.CharField(max_length=10, default='')
    B_negative_units = models.CharField(max_length=10, default='')
    AB_positive_units = models.CharField(max_length=10, default='')
    AB_negative_units = models.CharField(max_length=10, default='')
    O_positive_units = models.CharField(max_length=10, default='')
    O_negative_units = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.name

class Ambulance(models.Model):
    name = models.CharField(max_length=200,default=' ')
    state = models.CharField(max_length=100,default=' ')
    city = models.CharField(max_length=100,default=' ')
    vehicle_number = models.CharField(max_length=50,default=' ')
    mobile = models.CharField(max_length=100,default=' ')
    status = models.CharField(max_length=100,default=' ')
    hospital_name = models.CharField(max_length=100,default='')
    def __str__(self):
        return self.name

class Appointments(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    name = models.CharField(max_length=500,default=' ')
    bank_id = models.CharField(max_length=500,default=' ')
    on_date = models.DateField()
    service = models.CharField(max_length=500,default=' ')
    blood_type = models.CharField(max_length=100,default=' ')
    blood_units = models.CharField(max_length=100,default=' ')
    time_from = models.TimeField()
    time_to = models.TimeField()
    def __str__(self):
        return self.name

class Requests(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    bank_id = models.CharField(max_length=500,default=' ')
    service = models.CharField(max_length=500,default=' ')
    blood_units = models.CharField(max_length=500,default=' ')
    blood_type = models.CharField(max_length=500,default=' ')
    diseases = models.CharField(max_length=500,default=' ')
    request_message = models.TextField(default=' ')

class AnnouncementStaff(models.Model):
    message = message =models.TextField(default=' ')
    title = models.CharField(max_length=500,default=' ')
    admin_id = models.CharField(max_length=500,default=' ')
    staff_id = models.CharField(max_length=500,default=' ')

class MessageUser(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    admin_id = models.CharField(max_length=500,default=' ')
    staff_id = models.CharField(max_length=500,default=' ')
    sent_admin = models.BooleanField(default='False')
    date_send = models.DateField()
    message = models.TextField(default=' ')

class AddStaffRequest(models.Model):
    user_id = models.CharField(max_length=500,default=' ')
    admin_id = models.CharField(max_length=500,default=' ')
    blood_bank_name = models.CharField(max_length=500,default=' ')
    address = models.CharField(max_length=500,default=' ')
    state = models.CharField(max_length=100,default=' ')
    city = models.CharField(max_length=100,default=' ')
    mobile = models.CharField(max_length=100,default=' ')
    email = models.EmailField(default=' ')
    category = models.CharField(max_length=100,default=' ')
    status = models.CharField(max_length=100,default=' ')
    website = models.CharField(max_length=800,default=' ')
    blood_groups =  ListCharField(
        base_field=models.CharField(max_length=5),
        size=10,
        max_length=(10 * 10)  # 6 * 10 character nominals, plus commas,
    )
    A_positive_units = models.CharField(max_length=10, default='')
    A_negative_units = models.CharField(max_length=10, default='')
    B_positive_units = models.CharField(max_length=10, default='')
    B_negative_units = models.CharField(max_length=10, default='')
    AB_positive_units = models.CharField(max_length=10, default='')
    AB_negative_units = models.CharField(max_length=10, default='')
    O_positive_units = models.CharField(max_length=10, default='')
    O_negative_units = models.CharField(max_length=10, default='')
    date_send = models.DateField()
    request_message = models.TextField(default=' ')


