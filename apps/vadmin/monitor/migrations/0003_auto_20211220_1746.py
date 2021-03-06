# Generated by Django 2.2.16 on 2021-12-20 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20211212_0054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitor',
            options={'verbose_name': 'Monitor', 'verbose_name_plural': 'Monitor'},
        ),
        migrations.AlterModelOptions(
            name='sysfiles',
            options={'verbose_name': 'SysFiles', 'verbose_name_plural': 'SysFiles'},
        ),
        migrations.AlterField(
            model_name='monitor',
            name='cpu_num',
            field=models.CharField(max_length=8, verbose_name='CPU'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='cpu_sys',
            field=models.CharField(max_length=8, verbose_name='CPU'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='mem_num',
            field=models.CharField(max_length=32, verbose_name='Mem(KB)'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='mem_sys',
            field=models.CharField(max_length=32, verbose_name='MemSys(KB)'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='seconds',
            field=models.CharField(max_length=32, verbose_name='Seconds'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='server',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='monitor.Server', verbose_name='server'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='dir_name',
            field=models.CharField(max_length=32, verbose_name='dir_name'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='disk_sys',
            field=models.CharField(max_length=32, verbose_name='disk_sys(KB)'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='monitor',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='monitor.Monitor', verbose_name='monitor'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='sys_type_name',
            field=models.CharField(max_length=400, verbose_name='sys_type_name'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='total',
            field=models.CharField(max_length=32, verbose_name='total(KB)'),
        ),
        migrations.AlterField(
            model_name='sysfiles',
            name='type_name',
            field=models.CharField(max_length=32, verbose_name='type_name'),
        ),
    ]
