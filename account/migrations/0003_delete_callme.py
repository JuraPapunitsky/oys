# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150422_1445'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CallMe',
        ),
    ]
