# coding=utf-8

u"""
Утилиты, предназначенные для логгирования
"""

import logging
from datetime import datetime, date
import traceback
from crum import get_current_request
from lib.tasks import exec_rest


bps_logging_handler = logging.getLogger('bps_logging_handler')


class LogDataExtractMixin(object):
    u""" Примесь для вытаскивания данных из события """

    def get_data(self, record):
        """ Получить данные для отправки из записи события лога
        @arg record: Запись лога
        @return: dict
        """

        # Вычисляем extra-данные
        # как те, которых в стандартном наборе нет
        standard_attr = frozenset([
            'threadName', 'name', 'thread', 'created', 'process', 'processName',
            'args', 'module', 'filename', 'levelno', 'exc_text', 'pathname', 'lineno', 'msg',
            'exc_info', 'funcName', 'relativeCreated', 'levelname', 'msecs',
            # Переменные в extra докидывает сама django, но их мы тоже в логгер не берем
            'request', 'status_code', 'message', 'asctime'
        ])

        extra_data = {}
        for k, v in record.__dict__.items():
            if k not in standard_attr:
                # Иначе оно в JSON не запакуется при передаче
                if type(k) not in (str, int, float, date, datetime):
                    v = unicode(v)

                extra_data[k] = v

        # Если есть даннеые по исключению (exc_info)
        # Для ошибок пишем место ошибки, а не место ее логгирования
        # и сообщение ошибки, а не логгера

        if record.exc_info:
            exception_type, exception_value, tb = record.exc_info

            tb_frames = traceback.extract_tb(tb)
            pathname, lineno, function, code = tb_frames[-1]

            exception_info = '\n'.join(traceback.format_exception(exception_type, exception_value, tb))

            message = unicode(exception_value)
            message_pattern = message

            extra_data['logging_message'] = record.getMessage()

        else:
            pathname, lineno, function = record.pathname, record.lineno, record.funcName
            exception_info = getattr(record, 'exc_text', None)
            message, message_pattern = record.getMessage(), record.msg

        data = {
            'logger': record.name,
            'level': record.levelname,
            'message': message,
            'message_pattern': message_pattern,  # Передаем для улучшения группировки
            'pathname': pathname,
            'lineno': lineno,
            'function': function,
            'data': extra_data,
            'exception': exception_info,
            'stack': '\n'.join(traceback.format_stack()),
            'process_delay': getattr(self, '_process_delay', False),
        }

        # Добавим юзера, если есть
        request = getattr(record, 'request', get_current_request())
        if request:
            data['request'] = {
                'url': request.path[:1000],
                'get_args': request.GET.dict(),
                'post_args': request.POST.dict(),
                'method': request.method,
                'remote_addr': request.META['REMOTE_ADDR'],
            }

            user = getattr(request, 'user', None)
            if user and user.is_authenticated():
                data['request']['user_email'] = user.email
                data['request']['user_title'] = unicode(user)

        return data


class BPSHTTPLoggingHandler(LogDataExtractMixin, logging.Handler):
    """ Отправить сообщение в аггрегатор логов bps """

    def __init__(self, emit_delay=False, process_delay=False, error_email=True):
        u""" По умолчанию отправляем сообщения отложено через celery
        @emit_delay: Отправить сообщение отложено.
            Добавляет в цепочку доставки celery, но не вызывает блокировку
            из-за ожидания сети

        @process_delay: Обработать запись события в лог отложено при записи сообщения.
            Позволяет быстро отпустить задачу на стороне сервера хранения логов,
            но мы теряем обратную связь (успешно оно сохранилось или нет)

        Стандарные настройки позволяют получать обратную связь о том, что логи сохранены.
        если нагрузка сильно большая, то можно сначала выставить emit_delay,
        потом process_delay но возникает задача по обработке ошибок в celery.
        А их нужно обрабатывать без delay (если проблема в celery
        то ошибка до celery может и не дойти)
        """
        logging.Handler.__init__(self)
        self._emit_delay = emit_delay
        self._process_delay = process_delay
        self._error_email = error_email

    def emit(self, record):
        try:
            data = self.get_data(record)

            exec_rest_method = exec_rest
            if self._emit_delay:
                exec_rest_method = exec_rest_method.delay

            exec_rest_method(service='BPS_LOGGER',
                             path='logs/api/message/',
                             method='PUT',
                             data=data,
                             timeout=3)

        except Exception:
            bps_logging_handler.error('Send log message error', exc_info=True, extra={
                'request': getattr(record, 'request', None),
            })
            self.handleError(record)
