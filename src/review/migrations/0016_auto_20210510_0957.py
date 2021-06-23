# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-10 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0015_decisiondraft_editor_decline_rationale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisionrequest',
            name='author_note',
            field=models.TextField(blank=True, help_text='You can add an optional covering letter to the editor with details of the changes that you have made to your revised manuscript.', null=True, verbose_name='Covering Letter'),
        ),
    ]
