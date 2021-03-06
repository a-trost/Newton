# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-09 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ixl', '0005_ixlstats_ixl_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ixlstats',
            name='last_practiced',
            field=models.IntegerField(blank=True, default=20, verbose_name='Last Practiced'),
        ),
        migrations.AlterField(
            model_name='ixlstats',
            name='questions_answered',
            field=models.IntegerField(blank=True, default=0, verbose_name='Questions Answered'),
        ),
        migrations.AlterField(
            model_name='ixlstats',
            name='time_spent',
            field=models.IntegerField(blank=True, default=0, verbose_name='Time Spent'),
        ),
    ]
