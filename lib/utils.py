# coding=utf-8

u"""
Утилиты общего назначения
"""

from uuid import uuid4
import json
from requests import request
import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFile
from PIL.ExifTags import TAGS
from email.MIMEBase import MIMEBase
from email import Encoders
from uuid import uuid4
from lib.sms.prostor import JsonGate

# from django.contrib.sites.models import get_current_site as django_get_current_site

import re

from django.template import Template, Context
from django.http import QueryDict
from django.utils.encoding import force_unicode
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.conf import settings
from django.db import transaction
from django.apps import apps
from django.template.loader import render_to_string

from lib import logger_email
from lib.exception import RESTException

email_re = re.compile(r'[A-Z0-9+_\-\.]+@[0-9A-Z][\.\-0-9A-Z]*.[A-Z]+', re.IGNORECASE | re.MULTILINE)


def attribute_by_name(object_start, path):
    m = object_start
    for comp in path.split('.'):
        if type(m) in (dict, QueryDict,):
            m = m[comp]
        elif type(m) in (list, tuple,):
            m = m[int(comp)]
        else:
            m = getattr(m, comp)
    return m


def numformat(value, digits=2, delimiter='&nbsp;'):
    if value is None:
        return ''

    def numformat_format(val):
        v_list = list(val)
        for i in xrange((len(val) - 1) / 3):
            pos = len(val) - (i + 1) * 3
            v_list.insert(pos, delimiter)
        return "".join(v_list)

    value = round(value, digits)

    if digits == 0:
        return numformat_format('%.0f' % value)

    val_str = ('%.' + str(digits) + 'f') % (value,)
    val_1, val_2 = val_str.split('.')

    return numformat_format(val_1) + '.' + val_2


def xml_node(xml, path, attr=None):
    u"""
    Получает узел (один) XML по пути.
    Если его нет, возвращает None
    Служит для обеспечения читаемости кода
    """
    if xml is None:
        return None

    try:
        xml_node = xml.xpath(path)[0]
        if attr is not None:
            return getattr(xml_node, attr)
        return xml_node
    except:
        return None


def render_string(string_to_render, env={}):
    u""" Обрабатывает строку и возвращает строку """

    t = Template(string_to_render)
    return t.render(Context(env))


@transaction.atomic
def update_m2m(object, attr_name, items_new):
    u""" update m2m field into document """

    if type(items_new) != set:
        items_new = set(items_new)

    related_manager = getattr(object, attr_name)
    items_old = set([item.pk for item in related_manager.all()])

    tags_add = list(items_new - items_old)
    if tags_add:
        related_manager.add(*tags_add)

    tag_remove = list(items_old - items_new)
    if tag_remove:
        related_manager.remove(*tag_remove)


def cursor_result_dict(cursor):
    u"""
    Преобразует результат из [(1,2,3)] в [{'field1': 1, 'field2': 2, 'field2': 2}]
    """

    names = []
    for field in cursor.description:
        names.append(force_unicode(field[0]))

    rows = cursor.fetchall()

    return [dict(zip(names, row)) for row in rows]


def coalesce(*items):
    for item in items:
        if item is not None:
            return item


def formset_field_diff(data, initial):
    u''' Вычисляет различия между значением инициализации FormsetField и данными '''

    diff = []
    init_rows = len(initial) if initial else 0

    for i, row in enumerate(data):
        row_init = initial[i] if i < init_rows else {}
        if row == {}:
            continue

        deleted = row[u'DELETE']

        row_diff = {}
        for name, value in row.items():
            if name == u'DELETE':
                continue
            # Новая строка или измененная колонка
            if not row_init or value != row_init[name]:
                row_diff[name] = value

        if row_diff or deleted:
            diff.append({'id': row['id'], 'diff': row_diff, 'deleted': deleted})

    return diff


def send_mail(subject, body, recepients, files=None, content_files=None, html=True, draft=False, log=True, connection_name=None, cc=None):
    u'''
    Отправка почты в формате html с приложением файлов или файлового контента

    @arg content_files: [(name, content, mime)]
    @arg draft: Черновик. Не отправлять письмо, а просто собрать и вернуть его
    @arg log: Записать в лог отправляемое письмо

    @return: eml-контент. Может пригодиться или для расчета размера письма
        или для сохранения отправленного сообщения (по умолчанию, оно не сохраняется) '''

    from_email = settings.DEFAULT_FROM_EMAIL

    # Специальное соединение
    connection = None
    if connection_name and not draft:
        connection_conf = settings.EMAIL_CONNECTIONS[connection_name]
        connection = get_connection(**connection_conf)
        from_email = connection_conf['username']

    # Генерируем вручную, чтобы после отправки, можно было его получить
    # Если этого не делать, он каждый раз перегенерируется и невозможно понять, с каким id было по факту отправленно сообщение

    u = uuid4()
    prefix, domain = from_email.split('@')
    message_id = u'<%s@%s>' % (u.get_hex(), domain)
    headers = {
        'Message-Id': message_id,
    }

    msg = EmailMessage(subject=subject,
                       body=body,
                       from_email=from_email,
                       to=recepients,
                       connection=connection,
                       headers=headers,
                       # attachments=content_files,
                       cc=cc)
    if html:
        msg.content_subtype = 'html'

    if files:
        for files_obj in files:
            msg.attach_file(files_obj.path)

    if content_files:
        for content_file in content_files:
            # Хоть django поддерживает и простую передачу 3-х параметров
            # делаем именно через MIMEBase для поддержки не английского в названиях
            file_name, file_content, file_mime = content_file
            file_mime_app, file_mime_extension = file_mime.split('/')

            part = MIMEBase(file_mime_app, file_mime_extension)
            part.set_payload(file_content)
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name.encode('utf-8'))
            msg.attach(part)

    # Письмо может быть создано как черновик (и не отправляться)
    # Например, чтобы понять размер сообщения: float(len(msg.message().as_bytes()))
    if not draft:
        msg.send()

        if log:
            logger_email.info(subject, extra={
                'body': body,
                'subject': subject,
                'recepients': u', '.join(recepients),
                'message_id': message_id,
            })

    if connection:
        connection.close()

    return msg


def send_mail_template(subject, template_path, template_context, recepients,
                       files=[], content_files=[]):
    u''' Отправляет на почту письмо, полученое обработкой шаблона '''

    body = render_to_string(template_path, template_context)
    send_mail(subject, body, recepients, files=files, content_files=content_files)


def get_trace():

    import traceback
    import sys

    tr = []
    for st in traceback.format_exception(*sys.exc_info()):
        tr.append(st)

    return tr


def print_trace():
    print '-------------------'
    for l in get_trace():
        print l
    print '-------------------'


def parse_date(val):
    u"""
    Пытаемся преобразовать строку в дату,
    используя форматы из настроек
    """

    for format in settings.DATE_INPUT_FORMATS:
        try:
            return datetime.datetime.strptime(val, format).date()
        except:
            pass


def az_to_en(value):
    trans_map = {
        u'ğ': u'',
        u'ı': u'y',
        u'ö': u'u',
        u'g': u'e',
        u'ə': u'ya',
        u'ş': u'sh',
        u'a': u'a',
        u'c': u'g',
        u'b': u'b',
        u'e': u'e',
        u'd': u'd',
        u'ç': u'ch',
        u'f': u'f',
        u'i': u'i',
        u'h': u'sh',
        u'k': u'k',
        u'j': u'',
        u'm': u'm',
        u'l': u'l',
        u'o': u'o',
        u'n': u'n',
        u'q': u'g',
        u'p': u'p',
        u's': u's',
        u'r': u'p',
        u'u': u'u',
        u't': u't',
        u'v': u'v',
        u'y': u'y',
        u'x': u'h',
        u'z': u'z',
        u'ü': u'c',
    }
    res = []
    for ch in value:
        finded = trans_map.get(ch.lower())

        if finded is None:
            finded = ch.lower()

        else:
            if ch.isupper():
                finded = finded.upper()

        res.append(finded)

    return u''.join(res)


def get_model(app_label, model_name):
    return apps.get_model(app_label, model_name)


def add_image_watermark(in_file, text, out_file=None, angle=23, opacity=0.25):
    u""" Добавляет на всю картику водяной знак типа копирайта. """
    FONT = os.path.join(settings.BASE_DIR, 'static/lib/fonts/DejaVuSans.ttf')
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # Заворачиваем в ByteIO, чтоб не бить исходные изображения
    # если что-то пойдет не так
    img = Image.open(in_file)
    img = img.copy()

    img = img.convert('RGB')
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)

    while n_width + n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)

    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font)

    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)

    if out_file is None:
        out_file = in_file
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')


def add_image_text(in_file, text, out_file=None):
    u"""
    Добавить подпись в правом нижнем углу изображения
    белым текстом на черном фоне. Типа для даты и времени фотографии
    """
    FONT = os.path.join(settings.BASE_DIR, 'static/lib/fonts/DejaVuSans.ttf')

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    # Заворачиваем в ByteIO, чтоб не бить исходные изображения
    # если что-то пойдет не так
    img = Image.open(in_file)
    img = img.copy()

    img = img.convert('RGB')
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))

    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)

    watermark_width = watermark.size[0]

    # Увеличиваем размер шрифта, пока штамп не станет нормально влезать
    while n_width + n_height < watermark_width / 4:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)

    # Рисуем в нижнем правом углу с черной заливкой
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.rectangle([
        watermark.size[0] - n_width - 15,
        watermark.size[1] - n_height - 15,
        watermark.size[0] - 5,
        watermark.size[1] - 5,
    ], fill='#000000')
    draw.text(((watermark.size[0] - n_width - 10), (watermark.size[1] - n_height - 10)),
              text, font=n_font, fill='#ffffff')

    if out_file is None:
        out_file = in_file
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')


def get_image_tags(file_path):
    u""" Получить тэги изображения (EXIF) """
    img = Image.open(file_path)

    if not hasattr(img, '_getexif'):
        return {}

    info = img._getexif()
    if not info:
        return {}

    res = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        res[decoded] = value

    return res


def exec_rest(service, path, method, data, timeout=5):
    service_conf = getattr(settings, service)

    url = '%(service_url)s%(path)s' % {
        'service_url': service_conf['url'],
        'path': path,
    }

    data['api_key'] = service_conf['api_key']

    res = request(method=method,
                  url=url,
                  data=json.dumps(data),
                  headers={'content-type': 'application/json'},
                  timeout=timeout)

    # TODO: Сделать кастомное исключение с хранением детальной информации для логгирования
    # в любом месте трейса, где это исключение будет перехвачено
    if res.status_code != 200:
        raise RESTException(res.text)

    return res.json()


def sql_result_format(cursor):
    u""" Преобразовать запрос из списка кортежей (не именованных)
    в список словарей (в ключе названия колонок) """

    field_names = []
    for field in cursor.description:
        field_names.append(force_unicode(field[0]))

    result = cursor.fetchall()
    return [dict(zip(field_names, row)) for row in result]


def parse_regexp_groups(message, pattern, names, update_me=None):
    u""" Ищем в message pattern и возвращаем словарь, в котором names являются ключами """
    find = re.search(pattern, message)

    if find:
        find_groups = find.groups()

        if type(names) in (str, unicode):
            names = [names]

        res = {}
        for i, name in enumerate(names):
            res[name] = find_groups[i]

        if update_me:
            update_me.update(res)
            return True

        return res


def choices_with_nullable(choices):
    u""" Добавить к choices первой строкой ----
    чтоб можно было использовать в полях формы, где можно ее не указывать """

    new_choices = list(choices)
    new_choices.insert(0, ['', '----'])
    return new_choices


def send_sms(messages, queue_name=None, schedule_time=None):
    gate = JsonGate(login=settings.SMS_LOGIN, password=settings.SMS_PASSWORD)
    return gate.send(messages, queue_name, schedule_time)


class ObjectDict(dict):
    """
    Обертка над dict.

    Позволяет обращатся
    к ключам через вызов аттрибутов.
    Так код получается намного чище
    """

    def __init__(self, data):

        # Словари внутри превращаем тоже ObjectDict для навигации по точкам
        new_data = {}
        for k, v in data.items():
            if type(v) == dict:
                v = ObjectDict(v)

            new_data[k] = v

        super(ObjectDict, self).__init__(new_data)
        self.__dict__ = new_data


def get_uuid():
    """ Возвращает уникальный идентификатор в строковой форме.
    Используется для default параметров в моделях,
    когда нужно генерировать уникальный ключ при вставке.
    """
    return uuid4().hex
