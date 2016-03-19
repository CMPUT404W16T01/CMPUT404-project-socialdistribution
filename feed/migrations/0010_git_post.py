# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0009_foreignhost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Git_Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b' ', max_length=500)),
                ('date', models.CharField(default=b' ', max_length=500)),
                ('link', models.CharField(default=b' ', max_length=500)),
            ],
        ),
    ]
