# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 18:46
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('climate_data', '0007_es_load_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requests',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]