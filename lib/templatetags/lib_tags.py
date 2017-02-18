# coding=utf-8

import decimal
from math import ceil
from datetime import date, datetime
from collections import OrderedDict

from django import template
from django.forms import widgets
from django.db.models.query import QuerySet
from django.db.models import Model
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext as _
from crum import get_current_user
from crum import get_current_request


from lib.utils import numformat


register = template.Library()


def get_field_default_height(field):
    if issubclass(field.field.widget.__class__, widgets.Textarea):
        return 5
    elif issubclass(field.field.widget.__class__, widgets.SelectMultiple):
        return 4
    return 1


@register.simple_tag
def form_bootstrap(form, only_field_names=None, number_of_columns=1, layout='horizontal', label_weight=4, column_width=None):
    if not form:
        return ''

    field_weight = 12 - label_weight
    fields_column = []
    fields_row = []  # Поля, которые занимают всю строку выводятся внизу формы

    for field in form.visible_fields():

        if only_field_names and field.name not in only_field_names:
            continue

        # horizontal, row, vertical
        field_layout = layout
        if hasattr(field.field, 'layout'):
            if field.field.layout:
                field_layout = field.field.layout

        field_column = {"field": field, "layout": field_layout, "name": field.name, "label": field.label}

        if field_layout == u'row':
            fields_row.append(field_column)
            continue

        fields_column.append(field_column)

    # Вычисляем индексы перехода на новую колонку
    fields_per_column = int(ceil(len(fields_column) / float(number_of_columns)))
    fields_column_switch = [int(i * fields_per_column + fields_per_column) for i in xrange(number_of_columns - 1)]

    if column_width is None:
        column_width = 12 / number_of_columns

    return render_to_string('lib/forms/form.html',
                            {'form': form,
                             'fields_column': fields_column,
                             'fields_row': fields_row,
                             'layout': layout,
                             'fields_column_switch': fields_column_switch,
                             'column_width': column_width,
                             'label_weight': label_weight,
                             'field_weight': field_weight,
                             'show_hidden_fields': (only_field_names is None),
                             'is_form_standalone': (only_field_names is None)})


@register.simple_tag
def project_path():
    u""" return absolute path to project """

    return settings.BASE_DIR


@register.simple_tag
def smartbps_core_path():

    return settings.SMARTBPS_CORE_PATH


@register.simple_tag
def to_string(value, format=None, digits=None):
    u""" return absolute path to project """

    if value is None:
        return u''

    if digits is None:
        digits = 2

    t = type(value)

    def _to_date(v, format):
        if v.year <= 1900:
            return 'year=%s' % v.year
        return v.strftime(format)

    if t == bool and format is None or format == 'bool':
        return _(u'Да') if value else _(u'Нет')
    elif t == datetime and format is None or format == 'datetime':
        return _to_date(value, '%d.%m.%Y %H:%M')
    elif t == date and format is None or format == 'date':
        return _to_date(value, '%d.%m.%Y')
    elif t == int and format is None or format == 'int':
        return int(value)
    elif t in (float, long, decimal.Decimal) and format is None or format == 'float':
        return numformat(value, digits)
    elif t == QuerySet:
        return ", ".join([unicode(item) for item in value.all()])

    return unicode(value)


@register.simple_tag
def formset_bootstrap(formset):
    return render_to_string('templatetags/formset_bootstrap.html', {'formset': formset})


@register.simple_tag
def queryset_to_select_optgroup(queryset, group_by):
    groups = OrderedDict()  # {grouper_id: {'grouper_obj':N, 'list': N}}
    for item in queryset:

        grouper = getattr(item, group_by)
        key = grouper.id if grouper and issubclass(grouper.__class__, Model) else grouper

        if not key in groups:
            groups[key] = {'grouper': grouper, 'list': []}

        groups[key]['list'].append(item)

    return render_to_string('lib/templatetags/queryset_to_select_optgroup.html', {'groups': groups.values()})


@register.simple_tag(takes_context=True)
def pagination(context, page_obj):

    get = context['request'].GET.copy()

    # Оно будет в шаблоне установлено
    if 'page' in get:
        del get['page']

    query_string = get.urlencode()

    return render_to_string('lib/templatetags/pagination.html',
                            {'page_obj': page_obj, 'query_string': query_string})


@register.simple_tag
def site_url():
    return settings.SITE_URL


@register.simple_tag
def field_bootstrap(field):
    u'''
    Форматирует поле формы в поле bootstrap form.
    Применяется, если нужно поля формы раскладывать по экрану вручную,
    а не через form_bootstrap
    '''

    if not field:
        return u''
    return render_to_string('lib/forms/field_bootstrap.html', {'field': field})


@register.simple_tag
def string_repeat(char, count):
    return char * count


@register.assignment_tag
def crum_user():
    return get_current_user()


@register.assignment_tag
def crum_request():
    return get_current_request()


@register.simple_tag
def client_company_phone():
    return settings.CLIENT_COMPANY_PHONE
