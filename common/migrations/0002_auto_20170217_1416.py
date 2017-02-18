# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callme',
            name='d_call',
            field=models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0432\u043e\u043d\u043a\u0430'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='d_call_from',
            field=models.TimeField(verbose_name='\u0412\u0440\u0435\u043c\u044f \u0441'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='d_call_to',
            field=models.TimeField(verbose_name='\u0412\u0440\u0435\u043c\u044f \u0434\u043e'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='d_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u0418\u043c\u044f'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='callme',
            name='reason',
            field=models.PositiveSmallIntegerField(verbose_name='\u0422\u0435\u043c\u0430 \u0437\u0432\u043e\u043d\u043a\u0430', choices=[(1, '\u041a\u0443\u043f\u0438\u0442\u044c \u0441\u0442\u0440\u0430\u0445\u043e\u0432\u043a\u0443'), (2, '\u041e\u0431\u0441\u0443\u0434\u0438\u0442\u044c \u0443\u0441\u043b\u043e\u0432\u0438\u044f'), (3, '\u041f\u0440\u043e\u0447\u0435\u0435')]),
        ),
    ]
