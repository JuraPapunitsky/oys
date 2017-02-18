# coding=utf-8

u"""
Задачи, которые работают в асинхронном режиме или по расписанию
"""

from celery.task import task
from lib import models
from lib.sms_ata import AtaSmsService
from lib.utils import exec_rest as _exec_rest


@task
def check_sms_status():
    u"""
    Проверить статусы сообщений.

    Можно через сервис узнать статусы ВСЕХ сообщений в пачке.
    Поэтому вытаскиваем сообщения, у которых статус ожидания в очереди
    и достаем все пачки сообщений.
    И обновляем статусы уже по пачкам
    """
    messages_qs = models.SmsTaskMessage.objects.filter(status=1)
    task_qs = models.SmsTask.objects.filter(messages__in=messages_qs)

    # В одной пачке могут попасться несколько сообщений к обновлению
    task_qs = models.SmsTask.objects.filter(pk__in=task_qs)

    service = AtaSmsService()
    for sms_task in task_qs:
        if sms_task.external_id:
            service.refresh_status(task_id=sms_task.external_id)


@task
def exec_rest(service, path, data, method='POST', timeout=5):
    return _exec_rest(service=service, path=path, data=data, method=method, timeout=timeout)
