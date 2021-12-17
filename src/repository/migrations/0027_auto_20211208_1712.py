# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-08 17:12
from __future__ import unicode_literals

import core.model_utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0026_merge_20211011_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepositoryRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('author', 'Author')], max_length=20)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Repository')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='preprint',
            name='keywords',
            field=core.model_utils.M2MOrderedThroughField(blank=True, null=True, through='repository.KeywordPreprint', to='submission.Keyword'),
        ),
        migrations.AlterField(
            model_name='versionqueue',
            name='title',
            field=models.CharField(help_text='Your article title', max_length=300),
        ),
        migrations.AddField(
            model_name='repository',
            name='limit_access_to_submission',
            field=models.BooleanField(default=False,
                                      help_text='If enabled, users need to request access to submit preprints.'),
        ),
    ]
