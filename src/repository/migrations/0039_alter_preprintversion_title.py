# Generated by Django 3.2.20 on 2023-10-18 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0037_historicalrepository'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preprintversion',
            name='title',
            field=models.CharField(blank=True, default='', help_text='Your article title', max_length=300),
        ),
    ]
