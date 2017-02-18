# coding: utf-8

u"""
Менеджер сервисов Soap
Собирает со всех приложений сервисы и крутит их
"""

import logging
from importlib import import_module
import base64

from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase


from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse

from lib.utils import get_trace

logger = logging.getLogger('core.soap_service')


class ServiceAbstract(ServiceBase):
    u"""
    Базовый класс.

    Для всех сервисов с накрученными обработчиками исключений
    и прочими вещами глобального уровня
    """

    @classmethod
    def call_wrapper(cls, ctx):
        try:
            return super(ServiceAbstract, cls).call_wrapper(ctx)

        except Exception as e:
            logger.error(unicode(e), exc_info=True)
            raise e


def service_factory(service):
    u"""
    Оборачивает класс сервиса в приложение django c basic auth
    """

    application_tns = service.application_tns if hasattr(service, 'application_tns') else 'smartbps'
    service_name = service.service_name if hasattr(service, 'service_name') else service.__name__.lower()

    # 20 Мб
    max_content_length = (1024 * 1024 * 20)
    app = DjangoApplication(Application([service],
                                        tns=application_tns,
                                        name='smartbps',
                                        in_protocol=Soap11(validator='lxml'),
                                        out_protocol=Soap11()),
                            max_content_length=max_content_length)

    @csrf_exempt
    def service_wrapper(request):
        u"""
        При не авторизованном запросе (смотрим по сессии),
        выдаем запрос на авторизацию http401
        При получении ответа, запоминаем в сессию логин и пароль.
        Если в сессии есть логин-пароль, то проверяем его при каждом запросе
        (а вдруг поддерживается длинная сессия и пароль нужно поменять)
        """

        key = 'web_service:auth_%s' % service_name

        # Авторизован
        if key in request.session:
            uname, passwd = request.session[key]
            if uname == service.login and passwd == service.password:
                return app(request)

        # Обработка запроса авторизации
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                method, user_pass = auth
                if method == "Basic":
                    uname, passwd = base64.b64decode(user_pass).split(':')
                    if uname == service.login and passwd == service.password:
                        request.session[key] = [uname, passwd]
                        return app(request)

        # Нужно отправить запрос на авторизацию
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="soap_%s"' % service_name
        return response

    return service_wrapper


def get_services():
    u"""
    Перебираем установленные приложения и ищем в них модуль services.py
    В нем ищем классы сервисов, унаследованние от ServiceAbstract
    и на каждый из них создаем обертку с авторизацией, обработкой ошибок
    """

    services = {}
    for app_name in settings.INSTALLED_APPS:
        # Пробуем загрузить приложение
        try:
            module = import_module(app_name + ".services")
        except ImportError as e:
            if e.message != 'No module named services':
                raise e
            continue

        # В модуле ищем классы, унаследованные от ServiceAbstract
        for name in dir(module):
            obj = getattr(module, name)

            if isinstance(obj, type) and issubclass(obj, ServiceAbstract) and obj != ServiceAbstract:
                services[obj.__name__.lower()] = service_factory(obj)

    return services
