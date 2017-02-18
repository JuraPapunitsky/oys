# coding=utf-8

from lib.utils import render_string, attribute_by_name
import re
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.template import Context


class EnvirementManager(object):
    u"""
    Хранение параметров внутри объекта
    и различные методы, которые может выполнять объект с учетом хранимых переменных
    - обработку шаблонов
    - обработку текстов SQL-запроса
    """

    def __init__(self, **kwargs):

        self._env = kwargs

    def render(self, text, **dict):
        u""" Обработка строки шаблонной системой """
        try:
            return render_string(text, self._dict_mix(dict))

        except Exception as exc:
            return unicode(exc)

    def render_template_compiled(self, template, **dict):
        u""" Обработать предварительно скомпилированный шаблон """

        return template.render(Context(self._dict_mix(dict)))

    def render_template(self, path, **dict):
        u""" Обработать """

        return render_to_string(path, self._dict_mix(dict), context_instance=RequestContext(self._env['request']))

    def render_sql(self, sql, **dict):
        u"""  Обрабатывает строку шаблонной системой
        Возвращает обработанную строку и массив переменных для привязки """

        sql_rendered = self.render(sql, **dict)
        env_mixed = self._dict_mix(dict)
        binds = []

        sql_rendered = sql_rendered.replace('%', '%%')
        for bind_token in re.findall(r'\[{2}.+?\]{2}', sql_rendered):
            env_path = bind_token[2:-2]
            binds.append(attribute_by_name(env_mixed, env_path))
            sql_rendered = sql_rendered.replace(bind_token, u'%s')

        return (sql_rendered, binds)

    def _dict_mix(self, dict):

        if dict:
            e = self._env.copy()
            e.update(dict)
        else:
            e = self._env

        return e

    def get(self, name, value=None):

        return self._env.get(name, value)

    def __getitem__(self, name):

        return self._env[name]

    def __setitem__(self, name, value):

        self._env[name] = value
