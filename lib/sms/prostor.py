# coding=utf-8

import urllib
import json

import logging

logger = logging.getLogger('core.sms')


class JsonGate:
    """class for using prostor-sms.ru service via JSON interface"""

    _host = 'https://api.prostor-sms.ru/messages/v2'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    @property
    def balance(self):
        return self._send_request('balance', 'balance')

    def send(self, messages, queue_name=None, schedule_time=None):
        params = {
            'messages': messages,
            'statusQueueName': queue_name,
            'scheduleTime': schedule_time,
            'showBillingDetails': True,
        }
        try:
            response = self._send_request('send', ret_key='messages', params=params)
            logger.info('send messages', extra={
                'sms_messages': messages,
                'queue_name': unicode(queue_name),
                'scheduleTime': unicode(schedule_time),
                'response': response
            })
        except Exception as exc:
            logger.error(unicode(exc), exc_info=True, extra={
                'sms_messages': messages,
                'queue_name': unicode(queue_name),
                'scheduleTime': unicode(schedule_time),
            })

        return response

    def get_status(self, messages):
        params = {'messages': messages}
        return self._send_request('status', ret_key='messages', params=params)

    def senders(self):
        return self._send_request('senders')

    def _send_request(self, method, ret_key, params={}):
        url = '%s/%s.json' % (self._host, method)

        # Собираем параметры и пакуем в json
        data = {
            "login": self.login,
            "password": self.password,
        }
        for k, v in params.items():
            if v is not None:
                data[k] = v

        try:
            f = urllib.urlopen(url, json.dumps(data))
            result = f.read()
            response = json.loads(result)

            # print 'response', response

            if response['status'] != u'ok':
                raise Exception(response['description'])

            return response[ret_key]

        except Exception as exc:
            return {
                'error': unicode(exc)
            }

u"""
from lib.sms.prostor import JsonGate
gate = JsonGate('t89269347928', '785237')
print gate.balance
print gate.senders()

messages = [
    {
        "clientId": "2",
        "phone": "79269344424",
        "text": u"Тестовое сообщение",
        "sender": "Prostor"
    },
]

print gate.send(messages, 'testQueue')

print gate.status([
    {"clientId": "1", "smscId": 1778103308},
    {"clientId": "2", "smscId": 1778103307},
])

print gate.statusQueue('testQueue', 10)
"""
