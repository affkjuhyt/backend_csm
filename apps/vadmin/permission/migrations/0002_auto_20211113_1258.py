# Generated by Django 2.2.16 on 2021-11-13 05:58

import apps.vadmin.op_drf.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dept',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='user_create'),
        ),
        migrations.AlterField(
            model_name='dept',
            name='dept_belong_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Data attribution department'),
        ),
        migrations.AlterField(
            model_name='dept',
            name='description',
            field=apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='Description', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='dept',
            name='modifier',
            field=apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='The record was last modified by', max_length=255, null=True, verbose_name='editor'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='user_create'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='dept_belong_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Data attribution department'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='description',
            field=apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='Description', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='modifier',
            field=apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='The record was last modified by', max_length=255, null=True, verbose_name='editor'),
        ),
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='user_create'),
        ),
        migrations.AlterField(
            model_name='post',
            name='dept_belong_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Data attribution department'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='Description', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modifier',
            field=apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='The record was last modified by', max_length=255, null=True, verbose_name='editor'),
        ),
        migrations.AlterField(
            model_name='role',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='user_create'),
        ),
        migrations.AlterField(
            model_name='role',
            name='dept_belong_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Data attribution department'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='Description', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='role',
            name='modifier',
            field=apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='The record was last modified by', max_length=255, null=True, verbose_name='editor'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='user_create'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dept_belong_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Data attribution department'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=apps.vadmin.op_drf.fields.DescriptionField(blank=True, default='', help_text='Description', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='modifier',
            field=apps.vadmin.op_drf.fields.ModifierCharField(blank=True, help_text='The record was last modified by', max_length=255, null=True, verbose_name='editor'),
        ),
    ]