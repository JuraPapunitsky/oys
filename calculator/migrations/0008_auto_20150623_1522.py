# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_auto_20150617_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclecontract',
            name='delivery_region',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='region', choices=[(b'Bin\xc9\x99q\xc9\x99di', b'Bin\xc9\x99q\xc9\x99di'), (b'Yasamal', b'Yasamal'), (b'X\xc9\x99tai', b'X\xc9\x99tai'), (b'X\xc9\x99z\xc9\x99r', b'X\xc9\x99z\xc9\x99r'), (b'N\xc9\x99rimanov', b'N\xc9\x99rimanov'), (b'N\xc9\x99simi', b'N\xc9\x99simi'), (b'Nizami', b'Nizami'), (b'S\xc9\x99bail', b'S\xc9\x99bail'), (b'Sabun\xc3\xa7u', b'Sabun\xc3\xa7u'), (b'Suraxan\xc4\xb1', b'Suraxan\xc4\xb1'), (b'Qarada\xc4\x9f', b'Qarada\xc4\x9f'), (b'Pirallah\xc4\xb1', b'Pirallah\xc4\xb1'), (b'Dig\xc9\x99r', b'Dig\xc9\x99r')]),
        ),
        migrations.AlterField(
            model_name='vehiclecontract',
            name='delivery_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='delivery time interval', choices=[(1, b'09:00 - 10:00'), (2, b'10:00 - 11:00'), (3, b'11:00 - 12:00'), (4, b'12:00 - 13:00'), (5, b'13:00 - 14:00'), (6, b'14:00 - 15:00'), (7, b'15:00 - 16:00'), (8, b'16:00 - 17:00'), (9, b'17:00 - 18:00'), (10, b'18:00 - 19:00'), (11, b'19:00 - 20:00')]),
        ),
    ]
