# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 17:47
from __future__ import unicode_literals

import common.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climatedata',
            name='ann',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='apr',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='aug',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='aut',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='dec',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='feb',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='jan',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='jul',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='jun',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='mar',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='may',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='nov',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='oct',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='sep',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='spr',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='sum',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='climatedata',
            name='win',
            field=common.fields.CustomFloatField(blank=True, null=True),
        ),
    ]