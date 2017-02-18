# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


CALLME_REASON = (
    (1, _(u'Купить страховку')),
    (2, _(u'Обсудить условия')),
    (3, _(u'Прочее')),
)

RESPONSE_TYPE = (
    ('mobile', _(u'Мобильным телефоном')),
    ('email', _(u'Электронной почтой')),
)


class CallMe(models.Model):
    u""" Обращения для обратного звонка """

    d_create = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Дата создания'))
    name = models.CharField(max_length=50, verbose_name=_(u'Имя'))
    phone = models.CharField(max_length=50, verbose_name=_(u'Телефон'))
    d_call = models.DateField(verbose_name=_(u'Дата звонка'))
    d_call_from = models.TimeField(verbose_name=_(u'Время с'))
    d_call_to = models.TimeField(verbose_name=_(u'Время до'))
    reason = models.PositiveSmallIntegerField(choices=CALLME_REASON, verbose_name=_(u'Тема звонка'))