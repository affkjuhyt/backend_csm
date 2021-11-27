# Generated by Django 2.2.16 on 2021-11-27 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_group_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.CharField(choices=[(0, 'Enable'), (1, 'Disable')], default=0, max_length=20, verbose_name='status'),
        ),
    ]
