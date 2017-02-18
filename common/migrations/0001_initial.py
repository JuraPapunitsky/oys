# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallMe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('d_create', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('d_call', models.DateField()),
                ('d_call_from', models.TimeField()),
                ('d_call_to', models.TimeField()),
                ('reason', models.PositiveSmallIntegerField(choices=[(1, '\u0421\u0442\u0440\u0430\u0445\u043e\u0432\u0430\u043d\u0438\u0435'), (2, '\u0421\u0442\u0440\u0430\u0445\u043e\u0432\u0430\u043d\u0438\u04352'), (3, '\u0421\u0442\u0440\u0430\u0445\u043e\u0432\u0430\u043d\u0438\u04353')])),
            ],
        ),
    ]
