# Generated by Django 2.2.16 on 2022-01-14 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_postgroup_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgroup',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postgroup', to=settings.AUTH_USER_MODEL),
        ),
    ]
