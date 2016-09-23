# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-11 18:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('okcoder', '0005_levellog'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('status', models.IntegerField(default=0)),
                ('code', models.TextField()),
                ('partnership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='okcoder.Partnership')),
            ],
        ),
    ]
