# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0017_auto_20150805_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelcontract',
            name='d_rest_end',
        ),
        migrations.RemoveField(
            model_name='travelcontract',
            name='d_rest_start',
        ),
        migrations.AddField(
            model_name='travelcontract',
            name='d_end',
            field=models.DateField(null=True, verbose_name='contract date end', blank=True),
        ),
    ]
