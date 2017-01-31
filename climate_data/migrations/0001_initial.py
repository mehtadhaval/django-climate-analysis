# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 16:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClimateData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Tmax', 'Max Temp'), ('Tmin', 'Min Temp'), ('Tmean', 'Mean Temp'), ('Sunshine', 'Sunshine'), ('Rainfall', 'Rainfall')], max_length=32)),
                ('year', models.IntegerField()),
                ('unit', models.CharField(choices=[('Degrees C', 'Degrees C'), ('Total Hours', 'Degrees C'), ('mm', 'Degrees C')], max_length=32)),
                ('jan', models.FloatField(blank=True, null=True)),
                ('feb', models.FloatField(blank=True, null=True)),
                ('mar', models.FloatField(blank=True, null=True)),
                ('apr', models.FloatField(blank=True, null=True)),
                ('may', models.FloatField(blank=True, null=True)),
                ('jun', models.FloatField(blank=True, null=True)),
                ('jul', models.FloatField(blank=True, null=True)),
                ('aug', models.FloatField(blank=True, null=True)),
                ('sep', models.FloatField(blank=True, null=True)),
                ('oct', models.FloatField(blank=True, null=True)),
                ('nov', models.FloatField(blank=True, null=True)),
                ('dec', models.FloatField(blank=True, null=True)),
                ('win', models.FloatField(blank=True, null=True)),
                ('spr', models.FloatField(blank=True, null=True)),
                ('sum', models.FloatField(blank=True, null=True)),
                ('aut', models.FloatField(blank=True, null=True)),
                ('ann', models.FloatField(blank=True, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Region')),
            ],
            options={
                'verbose_name_plural': 'Climate Data',
                'verbose_name': 'Climate Data',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Tmax', 'Max Temp'), ('Tmin', 'Min Temp'), ('Tmean', 'Mean Temp'), ('Sunshine', 'Sunshine'), ('Rainfall', 'Rainfall')], max_length=32)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=32)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='common.Region')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
