# coding=utf-8

import json
import re
from collections import OrderedDict


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from lib.utils import get_model
from django.db.models import get_app, get_models
from django.db import connection
from .decorators import ajax_response
from django.utils.module_loading import import_by_path
from django.conf import settings
from django.utils import translation


def tree_widget(request, application, model_name):
    u""" Поставляет данные для иерархического поля """
    data = []

    if not request.is_ajax():
        return HttpResponseForbidden(u'Возможно обращение только по ajax')

    objects = get_model(application, model_name).objects

    node_id = request.GET['node_id']
    if node_id:
        objects = objects.filter(parent_id=node_id)
    else:
        objects = objects.filter(parent_id__isnull=True)

    for node in objects.iterator():
        title = unicode(node)
        has_children = node.children.exists()

        data.append({"id": node.id, "text": title, 'children': has_children, 'icon': False})

    return HttpResponse(json.dumps(data), content_type="application/json")


@ajax_response
def forms_widget_autocomplete(request):
    u'''
    Поставляет данные для поля - автоподстановка
    Забирает данные у функции-обработчика
    и отдает их для списка автодополнения
    '''

    if not request.is_ajax():
        return HttpResponseForbidden(u'Возможно обращение только по ajax')

    params = request.GET

    term = params.get('q')
    handler_path = params.get('handler_path')

    # Чистим лишние параметры для передачи в обработчик
    _params = {}
    for k in params.keys():
        if k in ('q', 'handler_path', '_'):
            continue
        _params[k] = params.get(k)

    handle_function = import_by_path(handler_path)
    res = handle_function(request=request, term=term, params=_params)

    return res


def db_documentation(request):
    u'''
    Собирает данные о представлении моделей
    в базе данных
    '''

    def _get_model_info(model):

        fields_meta = {}
        fields = model._meta.fields
        for field in fields:
            field_type = field.get_internal_type()

            ctx = {}

            if hasattr(field, 'max_length'):
                ctx.update({'max_length': field.max_length})

            if hasattr(field, 'max_digits') and hasattr(field, 'decimal_places'):
                ctx.update({'max_digits': field.max_digits, 'decimal_places': field.decimal_places})

            if hasattr(field, 'column'):
                ctx.update({'column': field.name})
            key = field.name + '_id' if field_type == 'ForeignKey' else field.name
            if field_type == 'ForeignKey':
                fields_meta[key] = {
                    'name': field.verbose_name,
                    'type': 'integer',
                    'is_null': field.null,
                    'db_table': field.rel.to._meta.db_table
                }
            else:
                type = connection.creation.data_types.get(field.__class__.__name__)
                type = str(type % ctx) if type else 'varchar(250)'
                try:
                    check = re.search(' CHECK(.+)', type)
                    if check.group(0):
                        check = check.group(0)
                        type = type.replace(check, '')
                except AttributeError:
                    check = ''
                fields_meta[key] = {
                    'name': field.verbose_name,
                    'type': type % ctx if type else 'FILE',
                    'is_null': field.null,
                    'check': check,
                }

        return {'db_table': model._meta.db_table,
                'verbose_name': model._meta.verbose_name,
                'docstring': model.__doc__,
                'fields': fields_meta}

    # Перебираем приложения
    applications = OrderedDict()
    for app_name in sorted(settings.INSTALLED_APPS):
        try:
            app = get_app(app_name)
        except:
            continue

        app_models_name = []
        app_models_data = {}

        for model in get_models(app):
            model_info = _get_model_info(model)
            db_table = model_info['db_table']

            app_models_name.append(db_table)

            app_models_data[db_table] = {
                'db_table': model_info['db_table'],
                'verbose_name': model_info['verbose_name'],
                'docstring': model_info['docstring'],
                'fields': model_info['fields']
            }

        if not app_models_name:
            continue

        sorted_models = [app_models_data[db_table_] for db_table_ in sorted(app_models_name)]

        applications[app_name] = sorted_models

    doc = render(request, 'lib/documentation.html', {'applications': applications})
    return doc


def set_lang(request, code):
    u""" Переключить язык и вернуться на предыдущий раздел """

    request.session[translation.LANGUAGE_SESSION_KEY] = code
    return HttpResponseRedirect(request.GET['back_url'])


def close_modal_window(request):
    return render(request, 'lib/close_modal_window.html')


def close_modal_window_no_reload(request):
    return HttpResponse('''
        <script>
            window.close()
        </script>
    ''')
