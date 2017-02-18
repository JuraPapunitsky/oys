# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_remove_carmodel_tag_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='car_type',
            field=models.ForeignKey(to='sale.CarType'),
        ),
    ]
