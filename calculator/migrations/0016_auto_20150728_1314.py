# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0015_travelcontract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelcontract',
            name='countries',
            field=models.TextField(null=True, verbose_name='countries', blank=True),
        ),
    ]
