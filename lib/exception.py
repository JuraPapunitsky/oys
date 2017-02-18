# coding=utf-8

import json


class CustomException(Exception):
    u"""
    Исключение.
    Нужно для разделения сообщения, которое показывается на экране
    и детальной информации, которая будет отправлена письмом администратору
    """

    def __init__(self, exception, detail):

        self.exception = exception
        self.detail = detail

    def format_html(self):
        return u'Ошибка: %s <br/>Информация: %s' % (self.exception, self.detail)


class RESTException(Exception):
    @property
    def json(self):
        return json.loads(self.message)
