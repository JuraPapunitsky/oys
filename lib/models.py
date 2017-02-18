# coding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class LogAccess(models.Model):
    u""" Тут лежат записи логгирования обращений к серверу """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             related_name='log_access')
    d_create = models.DateTimeField(null=False, auto_now_add=True)
    remote_addr = models.GenericIPAddressField(null=False)
    remote_host = models.CharField(max_length=100, null=True, blank=True)
    http_referer = models.CharField(max_length=1000, null=True, blank=True)
    path = models.CharField(max_length=1000, null=True, blank=True)
    post = models.TextField(null=True)

    class Meta:
        app_label = 'lib'


# Статусы доставки сообщений (возвращаются процедурой получения детального отчета)
SMS_STATUS = (
    (1, _('Message is queued')),
    (2, _('Message was successfully delivered')),
    (3, _('Message delivery failed')),
    (4, _('Message was removed from list')),
    (5, _('System error'))
)


class SmsTask(models.Model):
    u"""
    Задачи на отправку СМС
    """
    internal_id = models.CharField(max_length=36, db_index=True, null=True, blank=True,
                                   verbose_name=_('internal id'))
    external_id = models.CharField(max_length=50, db_index=True, null=True, blank=True,
                                   verbose_name=_('external task id'))
    sender_title = models.CharField(max_length=100, verbose_name=_('sender title'))
    task_type = models.CharField(max_length=50)

    class Meta:
        app_label = 'lib'


class SmsTaskMessage(models.Model):
    u"""
    Сообщения, отправляемые в рамках задачи на отправку
    """
    task = models.ForeignKey(SmsTask, related_name='messages')
    msisdn = models.CharField(max_length=12, verbose_name='ISDN', db_index=True)
    message = models.TextField(blank=True, null=True, verbose_name=_('message'))
    # Статус сообщений, собирается командами статуса
    status = models.PositiveIntegerField(default=1, verbose_name=_('status'), choices=SMS_STATUS)
    status_change = models.DateTimeField(auto_now_add=True, verbose_name=_('last status change'))
    # Системные поля
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_index=True, editable=False, verbose_name=_('created'))

    class Meta:
        app_label = 'lib'
