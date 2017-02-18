# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0005_smstaskmessage_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='smstask',
            name='task_type',
            field=models.CharField(default='birthday', max_length=50, choices=[(b'birthday', '\u0418\u0437\u0432\u0435\u0449\u0435\u043d\u0438\u0435 \u043e \u0434\u043d\u0435 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f'), (b'sale_policy', '\u0418\u0437\u0432\u0435\u0449\u0435\u043d\u0438\u0435 \u043e \u043f\u0440\u043e\u0434\u0430\u0436\u0435 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430')]),
            preserve_default=False,
        ),
    ]
