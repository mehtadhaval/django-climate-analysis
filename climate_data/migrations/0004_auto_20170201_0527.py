# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 05:27
from __future__ import unicode_literals

import common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_create_superuser'),
        ('climate_data', '0003_auto_20170131_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClimateTimeSeriesData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Tmax', 'Max Temp'), ('Tmin', 'Min Temp'), ('Tmean', 'Mean Temp'), ('Sunshine', 'Sunshine'), ('Rainfall', 'Rainfall')], max_length=32)),
                ('record_date', models.DateField()),
                ('measurement', common.fields.CustomFloatField(blank=True, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeseries_data', to='common.Region')),
            ],
            options={
                'verbose_name': 'Climate TimeSeries Data',
                'verbose_name_plural': 'Climate TimeSeries Data',
            },
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='climate_data', to='common.Region'),
        ),
    ]
