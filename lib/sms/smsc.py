# -*- coding: utf-8 -*-
# SMSC.RU API (smsc.ru) версия 1.8 (05.03.2015)

from requests import request


class Gate(object):
    def __init__(self, login, password):
        self._login = login
        self._password = password

    @property
    def balance(self):
        data = {
            'login': self._login,
            'psw': self._password,
            'cur': 'RUR',
            'fmt': '3'  # JSON
        }
        res = request(method='POST',
                      url='https://smsc.ru/sys/balance.php',
                      params=data)
        response = res.json()
        return float(response['balance'])

    def send(self, phone, message, check_balance=False, sms_id=None):
        data = {
            'login': self._login,
            'psw': self._password,
            'phones': phone,
            'charset': 'utf-8',
            'mes': message,
            'sender': '',  # Sender name
            'fmt': '3',  # JSON
            # 1 - не отправляет, а просто показывает стоимость
            # 2 - добавляет стоимость отправленного сообщения
            'cost': '1' if check_balance else '2',
            'maxsms': '5',

        }

        if sms_id:
            data['id'] = sms_id

        res = request(method='POST',
                      url='https://smsc.ru/sys/send.php',
                      params=data)

        response = res.json()
        if 'error_code' in response:
            raise Exception(response['error'])

        return {
            'cost': float(response['cost']),
            'cnt': response['cnt'],
            'id': response.get('id')
        }

    def get_status(self, phone, sms_id):
        data = {
            'login': self._login,
            'psw': self._password,
            'id': sms_id,
            'phone': phone,
            'fmt': '3',  # JSON
            # 'charset': 'utf-8',
        }

        res = request(method='POST',
                      url='https://smsc.ru/sys/status.php',
                      params=data)

        response = res.json()
        if 'error' in response:
            return {
                'error': response['error_code'],
                'error_message': response['error'],
            }

        else:
            status_map = {
                -3: 'message_not_found',
                -1: 'wait_send',
                0: 'sended',
                1: 'delivered',
                3: 'expired',
                20: 'cant_delivered',
                22: 'wrong_number',
                23: 'send_rejected',
                24: 'no_money',
                25: 'cant_send',
            }

            return {
                'error': response.get('err'),
                'status': status_map[response['status']],
            }


u"""

gate = Gate("dibrovsd@gmail.com", "")
gate.balance
gate.send('+79269344424', u'Проверка', check_balance=True)
gate.send('+79269344424', u'Проверка')
gate.get_status('+79269344424', 1)

"""
