# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0006_vehiclecontract_p2_inscompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclecontract',
            name='p11_id',
            field=models.PositiveIntegerField(null=True, verbose_name='p11 document id', blank=True),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='p12_id',
            field=models.PositiveIntegerField(null=True, verbose_name='p12 document id', blank=True),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='p2_id',
            field=models.PositiveIntegerField(null=True, verbose_name='p2 document id', blank=True),
        ),
    ]
