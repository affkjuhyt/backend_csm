# Generated by Django 2.2.16 on 2021-11-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_auto_20211127_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.IntegerField(choices=[(0, 'Enable'), (1, 'Disable')], default=0, verbose_name='status'),
        ),
    ]
