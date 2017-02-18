# coding=utf-8

import re
import decimal
import json
from collections import defaultdict
from django import template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()
from django.db.models.query import QuerySet
from datetime import date, datetime
from django.template.loader import render_to_string
from django import forms
from textile import textile as textile_parse
from lib.utils import numformat as numformat_formatter


# FIXME: Убрать это в пользу аналогичного тэга
@register.filter
def to_string(value, format=None):
    u""" Преобразует аргумент в строку """

    if value is None:
        return u''

    t = type(value)

    if t == bool and format is None or format == 'bool':
        return u'Да' if value else u'Нет'
    elif t == datetime and format is None or format == 'datetime':
        return value.strftime('%d.%m.%Y %H:%M')
    elif t == date and format is None or format == 'date':
        return value.strftime('%d.%m.%Y')
    elif t == int and format is None or format == 'int':
        return int(value)
    elif format == 'separate_int':
        return numformat_formatter(value, 0)
    elif t in (float, long, decimal.Decimal):
        return numformat_formatter(value, 2)

    return unicode(value)


@register.filter
def get_range(value):
    u""" Возвращает список длинной value: 3|range => [1,2,3] """
    return range(1, value + 1)


@register.filter(is_safe=True)
def numformat(value, arg=0):
    """
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    """

    if value is None:
        return ''

    return mark_safe(numformat_formatter(value, arg))



@register.filter
def to_javascript_value(value, enclosure='"'):
    u""" Преобразовывает значение для вставки в javascript-код """

    # логическое
    # число
    # словарь
    # массив
    if value in ('true', 'false') or value.replace('.', '', 1).isdigit() \
        or value[0] == '{' and value[-1:] == '}' \
        or value[0] == '[' and value[-1:] == ']':
        return value

    return '%s%s%s' % (enclosure, value, enclosure)


@register.filter
def number_to_verbose(num):
    '''
    Склоняем словоформу
    @ author runcore
    '''

    def morph(n, f1, f2, f5):

        n = abs(int(n)) % 100
        if n > 10 and n < 20:
            return f5

        n = n % 10
        if n > 1 and n < 5:
            return f2
        if n == 1:
            return f1

        return f5

    if not num:
        return ''

    num = str(num)
    mapping = [(',', '.'), (' ', ''), ]
    for k, v in mapping:
        num = num.replace(k, v)

    nul = 'ноль'
    ten = (
        ('', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять'),
        ('', 'одна', 'две', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять'),
    )
    a20 = (
    'десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать',
    'восемнадцать', 'девятнадцать')
    tens = {2: 'двадцать', 3: 'тридцать', 4: 'сорок', 5: 'пятьдесят', 6: 'шестьдесят', 7: 'семьдесят', 8: 'восемьдесят',
            9: 'девяносто'}
    hundred = ('', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот')
    unit = (
        ('копейка', 'копейки', 'копеек', 1),
        ('рубль', 'рубля', 'рублей', 0),
        ('тысяча', 'тысячи', 'тысяч', 1),
        ('миллион', 'миллиона', 'миллионов', 0),
        ('миллиард', 'милиарда', 'миллиардов', 0),
    )

    rub, kop = ("%015.2f" % float(num)).split('.')
    out = [];
    if (int(rub) > 0):

        rub_by3 = []
        rub_cp = rub
        for i in xrange(len(rub_cp) / 3):
            rub_by3.append(rub_cp[0:3])
            rub_cp = rub_cp[3:]

        for uk in xrange(len(rub_by3)):

            v = rub_by3[uk]

            if not int(v):
                continue;

            uk = len(unit) - uk - 1;
            gender = unit[uk][3];
            i1, i2, i3 = map(int, v)

            #mega-logic
            out.append(hundred[i1]) # 1xx-9xx
            if i2 > 1:
                out.append(tens[i2] + ' ' + ten[gender][i3]) # 20-99
            else:
                out.append(a20[i3] if i2 > 0 else ten[gender][i3]) # 10-19 | 1-9
                #units without rub & kop
            if uk > 1:
                out.append(morph(v, unit[uk][0], unit[uk][1], unit[uk][2]))

    else:
        out.append(nul)

    out.append(morph(int(rub), unit[1][0], unit[1][1], unit[1][2])) #rub
    out.append(kop + ' ' + morph(kop, unit[0][0], unit[0][1], unit[0][2])) #kop
    return re.sub(r' {2,}', ' ', ' '.join(out)).strip();


'''
Преобразовать строку даты в формате dd.mm.yyyy в dd month yyyy
с учетом склонений названий месяцев
'''


@register.filter
def date_humanize(date_str):
    if not date_str:
        return ''

    date_str = date_str.strftime('%d.%m.%Y')

    month_names = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая',
                   '06': 'июня', '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября',
                   '12': 'декабря'}
    split_date = date_str.split('.')
    split_date[1] = month_names[split_date[1]]
    return ' '.join(split_date)


@register.filter
def paginator(page_obj):
    return render_to_string('filter/paginator.html', {'page_obj': page_obj})


@register.filter
def textile(string):
    return textile_parse(string)


@register.filter
def widget_readonly(form_field):

    field = form_field.field
    widget = field.widget

    if hasattr(widget, 'widgets'):
        for subwidget in widget.widgets:
            subwidget.attrs['readonly'] = True
    else:
        widget.attrs['readonly'] = True

    return form_field


@register.filter
def to_bootstrap_widget(form_field):

    field = form_field.field
    widget = field.widget

    def to_bootstrap(w):

        css_class = w.attrs.get('class')
        bootstrap_style = w.attrs.get('bootstrap_style', 'true')
        widget_type = type(w)

        if bootstrap_style == 'true' and widget_type not in (forms.CheckboxInput, forms.CheckboxSelectMultiple):
            if css_class is None:
                css_class = "form-control"
            else:
                css_class = '%s %s' % (css_class, "form-control")

        w.attrs['class'] = css_class

    if hasattr(widget, 'widgets'):
        for subwidget in widget.widgets:
            to_bootstrap(subwidget)
    else:
        to_bootstrap(widget)

    return form_field



@register.filter
def mptt_path(obj, delimiter='/'):
    options = [unicode(node) for node in obj.get_ancestors()]
    options.append(unicode(obj))
    return (" %s " % delimiter).join(options)


@register.filter
def undeleted_queryset(queryset):

    if type(queryset) == QuerySet:
        return queryset.filter(deleted=False)

    return queryset

@register.filter
def order_queryset(queryset, order_string):

    if type(queryset) == QuerySet:
        order_fields = order_string.split(',')
        return queryset.order_by(*order_fields)

    return queryset

@register.filter
def to_xml(xml_string):
    if not xml_string:
        return []

    from lxml import etree
    return etree.fromstring(xml_string)

@register.filter
def xpath(xml, path):
    finds = xml.xpath(path)
    if finds:
        return finds[0]
    return None

@register.filter
def to_json(val):
    if val:
        return json.dumps(val)
    return ''

@register.filter
def number_to_rur(val):
    u""" Преобразовать число в формат 999 руб. 00 коп. """

    if not val:
        return u'0 руб. 00 коп.'

    parts = str(val).split('.')
    if parts:
        if len(parts) == 2:
            return u'%s руб. %s коп.' % (parts[0], parts[1])
        if len(parts) == 1:
            return u'%s руб. 00 коп.' % parts[0]



