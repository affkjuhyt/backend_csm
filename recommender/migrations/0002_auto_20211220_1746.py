# Generated by Django 2.2.16 on 2021-12-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldasimilarity',
            name='created',
            field=models.DateField(blank=True, null=True),
        ),
    ]
