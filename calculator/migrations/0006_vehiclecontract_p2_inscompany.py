# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0005_auto_20150605_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclecontract',
            name='p2_inscompany',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='insurance company', blank=True),
        ),
    ]
