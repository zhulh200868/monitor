# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20150118_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor_meg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=20)),
                ('service_name', models.CharField(max_length=20)),
                ('num', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
