# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-29 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20200529_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='orcid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
