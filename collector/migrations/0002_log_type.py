# Generated by Django 2.2.16 on 2022-01-14 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
