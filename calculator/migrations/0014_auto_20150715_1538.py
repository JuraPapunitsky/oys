# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0013_auto_20150710_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclecontract',
            name='ateshgah_beshlik',
            field=models.BooleanField(default=False, verbose_name='ateshgah beshlik'),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='ateshgah_icbariplus',
            field=models.BooleanField(default=False, verbose_name='ateshgah icbariplus'),
        ),
        migrations.AddField(
            model_name='vehiclecontract',
            name='ateshgah_superkasko',
            field=models.BooleanField(default=False, verbose_name='ateshgah superkasko'),
        ),
    ]
