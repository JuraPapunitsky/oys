# coding=utf-8

u"""
Методы, которые перехватывают и обрабатывают запросы к серверу
"""

import json

# from django.conf import settings
from lib.models import LogAccess


class LogAccessMiddleware(object):
    u""" Логгирует все обращения к серверу в таблицу """
    def process_request(self, request):
        # Сюда постоянно долбится обновление списка звонков
        if request.path in ('/call_info/', '/crm/call_info/'):
            return

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        if request.method == 'POST':
            post = json.dumps(dict(request.POST), ensure_ascii=False)
        else:
            post = None

        http_referer = request.META.get('HTTP_REFERER')
        if http_referer:
            http_referer = http_referer[:1000]

        log_record = LogAccess(user=user,
                               remote_addr=request.META['REMOTE_ADDR'],
                               remote_host=request.META.get('REMOTE_HOST'),
                               http_referer=http_referer,
                               path=request.path[:1000],
                               post=post)

        log_record.save(force_insert=True)


class CookiesAddInfo(object):
    u"""
    Добавляет в сессию пользователя доп. информацию.
    Это нужно, чтоб при возникновении ошибки было понятно,
    у кого она произошла (в письме с ошибкой сессия не присылается,
    но присылается содержимое сесии)
    """

    def process_request(self, request):
        user = request.user
        if user.is_authenticated() and 'user_email_debug' not in request.COOKIES:
            request.COOKIES['user_email_debug'] = request.user.email
