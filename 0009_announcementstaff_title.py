# Generated by Django 5.0.6 on 2024-05-18 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0008_announcementstaff_staff_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcementstaff',
            name='title',
            field=models.CharField(default=' ', max_length=500),
        ),
    ]
