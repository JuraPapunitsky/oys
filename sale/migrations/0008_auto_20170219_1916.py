# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0007_auto_20170219_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdata',
            name='car_model',
            field=models.ForeignKey(to='sale.CarModel'),
        ),
    ]
