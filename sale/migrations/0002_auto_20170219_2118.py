# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientdata',
            old_name='registration_numbe',
            new_name='registration_number',
        ),
    ]
