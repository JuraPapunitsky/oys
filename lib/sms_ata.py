# coding=utf-8

import uuid
import urllib2
import logging
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from lxml import etree
from django.conf import settings
from crum import get_current_request
from lib.models import SmsTask, SmsTaskMessage


logger = logging.getLogger('core.sms_ata')


class SmsError(Exception):
    codes = {
        '001': u'Processing, report is not ready',
        '002': u'Duplicate <control_id>',
        '100': u'Bad request',
        '101': u'Operation type is empty',
        '102': u'Invalid operation',
        '103': u'Login is empty',
        '104': u'Password is empty',
        '105': u'Invalid authentication information',
        '106': u'Title is empty',
        '107': u'Invalid title',
        '108': u'Task id is empty',
        '109': u'Invalid task id',
        '110': u'Task with supplied id is canceled',
        '111': u'Scheduled date is empty',
        '112': u'Invalid scheduled date',
        '113': u'Old scheduled date',
        '114': u'isbulk is empty',
        '115': u'Invalid isbulk value, must “true” or “false”',
        '116': u'Invalid bulk message',
        '117': u'Invalid body',
        '118': u'Not enough units',
        '235': u'Invalid TITLE please contact Account Manager',
        '2XX': u'System error, report to administrator',
        '300': u'Internal server error, report to administrator'
    }

    def __init__(self, code):
        message = SmsError.codes.get(code)
        super(SmsError, self).__init__(message)


class AtaSmsService(object):
    u"""
    Класс обертка для сервиса отправки смс компании ATA Texnologiya
    """
    def __init__(self):
        self._sender_title = settings.ATA_SENDER_TITLE
        self._url = settings.ATA_SMS_URL
        self._login = settings.ATA_SMS_LOGIN
        self._pwd = settings.ATA_SMS_PASSWORD

    @staticmethod
    def _append_elements(node, elements_dict):
        u"""
        Добавляет в узел {node} дочерние узлы, собирая их из словаря {elements_dict}
        :param node: целевой узел
        :param elements_dict: словарь с данными для создания дочерних узлов
        :return: исходный узел
        """
        for k, v in elements_dict.items():
            sn = etree.Element(k)
            if isinstance(v, bool):
                v = 'true' if v else 'false'
            elif isinstance(v, datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            elif v is None:
                v = ''
            else:
                v = unicode(v)
            sn.text = v
            node.append(sn)
        return node

    @staticmethod
    def _get_head(**kwargs):
        u"""
        Заголовок для запроса
        :param kwargs: ключи - теги xml, занчения - текст тега
        :return: ноду дерева etree
        """
        return AtaSmsService._append_elements(etree.Element('head'), kwargs)

    def _send_request(self, xml_tree):
        u"""
        Запрос к API сервиса отправки сообщений
        :param xml_tree:
        :return:
        """
        if settings.ATA_SMS_DEBUG:
            raise Exception('Only for SMS_ATA_DEBUG = False')

        r = urllib2.Request(
            url=self._url, headers={'Content-Type': 'application/xml'},
            data=etree.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        )
        u = urllib2.urlopen(r)
        resp_body = u.read()
        resp_xml = etree.fromstring(resp_body)
        try:
            resp_code = resp_xml.xpath('/response/head/responsecode')[0].text
        except:
            resp_code = None

        return resp_code, resp_xml

    def submit_bulk(self, task_type, message, recipient_isdns, schedule=None):
        u"""
        Массовая рассылка одногоо сообщения списку получателей
        :param sender_title: доступное имя отправителя (из вызова метода get_titles())
        :param message: текст сообщения
        :param recipient_isdns: список номеров телефонов
        :param schedule: дата и время отоложенной отправки сообщения (по Баку)
        :return:
        """
        if settings.ATA_SMS_DEBUG:
            return

        if not schedule:
            schedule = datetime.now()

        if not recipient_isdns:
            return

        control_id = unicode(uuid.uuid4())

        # Готовим xml-стуктуру для запроса
        request = etree.Element('request')
        request.append(self._get_head(operation='submit',
                                      login=self._login,
                                      password=self._pwd,
                                      title=self._sender_title,
                                      scheduled=schedule,
                                      isbulk=False,
                                      controlid=control_id))

        for isdn in recipient_isdns:
            body = etree.Element('body')

            self._append_elements(body, {
                'msisdn': isdn,
                'message': message
            })

            request.append(body)

        resp_code, resp_xml = self._send_request(request)

        if resp_code == '000':

            # Получение идентификатора задачи во внешней системе
            task_id = resp_xml.xpath('/response/body/taskid')[0].text

            # Логируем отправленные сообщения
            with transaction.atomic():
                task = SmsTask(internal_id=control_id,
                               task_type=task_type,
                               external_id=task_id,
                               sender_title=self._sender_title)
                task.save()

                for isdn in recipient_isdns:
                    task_msg = SmsTaskMessage(msisdn=isdn, message=message, task=task)
                    task_msg.save()

            return task_id
        else:
            raise SmsError(code=resp_code)

    def submit(self, task_type, messages, schedule=None):
        u"""
        Рассылка одиночных сообщений
        :param sender_title: доступное имя отправителя (из вызова метода get_titles())
        :param messages: список кортежей вида [(<номер телефона>, <текст сообщения>), ... ]
        :param schedule: дата и время отоложенной отправки сообщения (по Баку)
        :return:
        """

        if settings.ATA_SMS_DEBUG:
            return

        if not messages:
            return

        if not schedule:
            schedule = datetime.now()

        control_id = unicode(uuid.uuid4())

        resp_code, xml_response, xml_request = None, None, None
        try:

            # Готовим xml-стуктуру для запроса
            xml_request = etree.Element('request')
            xml_request.append(self._get_head(operation='submit',
                                          login=self._login,
                                          password=self._pwd,
                                          title=self._sender_title,
                                          scheduled=schedule,
                                          isbulk=False,
                                          controlid=control_id))

            for isdn, message in messages:
                body = etree.Element('body')
                self._append_elements(body, {'msisdn': isdn, 'message': message})
                xml_request.append(body)

            # Отправка запроса
            resp_code, xml_response = self._send_request(xml_request)

            if resp_code == '000':
                task_id = xml_response.xpath('/response/body/taskid')[0].text

                # Логируем отправленные сообщения
                with transaction.atomic():
                    task = SmsTask(internal_id=control_id,
                                   task_type=task_type,
                                   external_id=task_id,
                                   sender_title=self._sender_title)
                    task.save()

                    for isdn, message in messages:
                        task_msg = SmsTaskMessage(msisdn=isdn, message=message, task=task)
                        task_msg.save()

                return task_id
            else:
                raise SmsError(code=resp_code)

        except Exception as e:
            logger.error(u'Ошибка отправки CMS: %s' % e, exc_info=True, extra={
                'request': get_current_request(),
                'xml_request': etree.tostring(xml_request, pretty_print=True),
                'xml_response': etree.tostring(xml_response, pretty_print=True),
            })
            raise e

    def get_short_report(self, task_id):
        u"""
        Крыткий отчет по отправке
        :param task_id: идентификатор задачи во внешней системе
        :return:
        """

        if settings.ATA_SMS_DEBUG:
            return

        request = etree.Element('request')
        request.append(self._get_head(operation='report',
                                      login=self._login,
                                      password=self._pwd,
                                      taskid=task_id))

        resp_code, resp_xml = self._send_request(request)

        if resp_code == '000':
            statuses = {
                'pending': int(resp_xml.xpath('/response/body/pending')[0].text),
                'delivered': int(resp_xml.xpath('/response/body/delivered')[0].text),
                'failed': int(resp_xml.xpath('/response/body/failed')[0].text),
                'removed': int(resp_xml.xpath('/response/body/removed')[0].text),
                'error': int(resp_xml.xpath('/response/body/error')[0].text),
            }
            return statuses
        else:
            raise SmsError(code=resp_code)

    def get_detailed_report(self, task_id):
        u"""
        Подробный отчет
        :param task_id: идентификатор задачи во внешней системе
        :return:
        """

        if settings.ATA_SMS_DEBUG:
            return

        request = etree.Element('request')
        request.append(self._get_head(operation='detailedreport',
                                      login=self._login,
                                      password=self._pwd,
                                      taskid=task_id))

        resp_code, resp_xml = self._send_request(request)

        if resp_code == '000':
            messages = []
            for msg in resp_xml.xpath('/response/body'):
                messages.append({
                    'msisdn': msg.xpath('msisdn')[0].text,
                    'message': msg.xpath('message')[0].text,
                    'status': int(msg.xpath('status')[0].text)
                })

            return {
                'task_id': task_id,
                'messages': messages,
            }

        else:
            raise SmsError(code=resp_code)

    def get_units(self):
        u"""
        Запрос оставшихся оплаченных сообщений
        :return:
        """
        request = etree.Element('request')
        request.append(self._get_head(operation='units', login=self._login, password=self._pwd))

        resp_code, resp_xml = self._send_request(request)

        if resp_code == '000':
            units = int(resp_xml.xpath('/response/body/units')[0].text)
            return units
        else:
            raise SmsError(code=resp_code)

    def get_titles(self):
        u"""
        Запрос зарегистрированных на пользователя названий для отправки
        :return:
        """
        request = etree.Element('request')
        request.append(self._get_head(operation='titles', login=self._login, password=self._pwd))

        resp_code, resp_xml = self._send_request(request)

        if resp_code == '000':
            titles = [t.text for t in resp_xml.xpath('/response/title')]
            return titles
        else:
            raise SmsError(code=resp_code)

    def refresh_status(self, task_id, message_id=None):
        u"""
        Обновить статусы отправки сообщений по задаче
        :param task_id: идентификатор задачи во внешней системе
        :return:
        """
        if settings.ATA_SMS_DEBUG:
            return

        report = self.get_detailed_report(task_id)
        report_messages = {m['msisdn']: m['status'] for m in report['messages']}

        task = SmsTask.objects.get(external_id=task_id)
        message_qs = task.messages.all()

        # Если запрошено конкретное сообщение, чтобы не обновлять всю кучу
        if message_id:
            message_qs = message_qs.filter(pk=message_id)

        for m in message_qs:
            if m.msisdn in report_messages:
                m.status = report_messages[m.msisdn]
                m.status_change = timezone.now()
                m.save()
