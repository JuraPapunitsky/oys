# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0006_auto_20170219_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientdata',
            name='car_engine',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientdata',
            name='car_size',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientdata',
            name='car_weight',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clientdata',
            name='car_model',
            field=models.CharField(max_length=200),
        ),
    ]
