# Generated by Django 2.2.16 on 2021-12-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_auto_20211220_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldasimilarity',
            name='created',
            field=models.DateField(),
        ),
    ]
