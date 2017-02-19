# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_doctype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarTypeCarModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='carmodel',
            name='car_type',
        ),
        migrations.AlterField(
            model_name='clientdata',
            name='car_type',
            field=models.ForeignKey(to='sale.TransportType'),
        ),
        migrations.DeleteModel(
            name='CarType',
        ),
        migrations.AddField(
            model_name='cartypecarmodel',
            name='car_model',
            field=models.ForeignKey(to='sale.CarModel'),
        ),
        migrations.AddField(
            model_name='cartypecarmodel',
            name='transport_type',
            field=models.ForeignKey(to='sale.TransportType'),
        ),
    ]
