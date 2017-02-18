# coding=utf-8
import pickle
import base64
import hashlib
from suds.client import Client
from django.conf import settings
from django.core.cache import cache


class BunchObject(dict):
    u"""
    Словарь с доступом к элементам через аттрибуты объекта
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super(BunchObject, self).__init__(**kwargs)


class GetClassifier(object):
    u"""
    Обертка получения словаря через сервис с кэшированием результатов
    """
    def __init__(self, model_name):
        self._soap_client = None
        self._model_name = model_name
        self._ops = []

    def _get_soap(self):
        if self._soap_client is None:
            # Инициализация клиента SOAP
            self._soap_client = Client(settings.ASAN_SVC_URL, username=settings.ASAN_SVC_USER,
                                       password=settings.ASAN_SVC_PWD)
        return self._soap_client

    def filter(self, *args, **kwargs):
        self._ops.append(('filter', args, kwargs))
        return self

    def exclude(self, *args, **kwargs):
        self._ops.append(('exclude', args, kwargs))
        return self

    def distinct(self, *args, **kwargs):
        self._ops.append(('distinct', args, kwargs))
        return self

    def order_by(self, *args, **kwargs):
        self._ops.append(('order_by', args, kwargs))
        return self

    def execute(self):
        p_ops = pickle.dumps(self._ops)
        b64_ops = base64.b64encode(p_ops)

        m = hashlib.md5()
        m.update(b64_ops)
        cache_key = '%s:%s' % (self._model_name, m.hexdigest())

        # Кэширование результата запроса
        result = cache.get(cache_key)
        if not result:
            response = self._get_soap().service.get_classifier(self._model_name, b64_ops)
            result = [{'id': r.id, 'title': unicode(r.title)} for r in response.ClassifierRecord]
            cache.set(cache_key, result, 3600)

        self._ops = []
        return [BunchObject(**r) for r in result]
