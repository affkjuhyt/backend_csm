# Generated by Django 2.2.16 on 2021-12-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0002_auto_20211220_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldasimilarity',
            name='created',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
