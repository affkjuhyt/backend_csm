# Generated by Django 2.2.16 on 2021-11-27 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0007_userprofile_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='group',
        ),
    ]
