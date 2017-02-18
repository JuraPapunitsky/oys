# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0003_smstask_smstaskmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smstask',
            name='sender_title',
            field=models.CharField(max_length=100, verbose_name='sender title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smstaskmessage',
            name='task',
            field=models.ForeignKey(related_name='messages', to='lib.SmsTask'),
            preserve_default=True,
        ),
    ]
