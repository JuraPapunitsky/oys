# coding=utf-8
import hashlib
import os
import mechanize
import random
import time
from datetime import datetime
from bs4 import BeautifulSoup

from PIL import Image
import pytesseract
from django.core.cache import cache

USER_AGENTS = (
    # IE
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
    # Chrome
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    # FF
    'Mozilla/5.0 (X11; U; Linux i686; az-AZ; rv:1.9.0.3) Gecko/2008092816',
)


class StatusCodeError(StandardError):
    """
    Status other than 200
    """
    pass


class PageError(StandardError):
    """
    Error in received page
    """
    pass


class ISBError(Exception):
    pass


class ISBParser(object):
    u"""
    ISB Parser
    """
    _service_url = 'http://services.isb.az/Cmtpl/CheckValidityBM.aspx'
    _captcha_fp = './last_captcha.png'
    _br = None
    _last_response = None

    def __init__(self):
        self._br = mechanize.Browser()  # Browser
        self._br.set_handle_equiv(True)
        self._br.set_handle_redirect(True)
        self._br.set_handle_referer(True)
        self._br.set_handle_robots(False)
        self._br.set_handle_redirect(mechanize.HTTPRedirectHandler)
        self._br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)

    def _save_captcha(self, path):
        u""" Сохранить капчу по указанному пути """
        soup = BeautifulSoup(self._last_response.get_data(), 'lxml')

        # Ищем контейнер с капчей и выкачиваем ее
        img = soup.find('img', id='cap')
        print 'img', img
        image_response = self._br.open_novisit(img['src'])

        # Сохраняем что выкачали
        with open(path, 'w') as captcha_image:
            captcha_image.write(image_response.read())

    def _parse_search_result(self, html_data=''):
        u"""
        Gets resulting data
        :return:
        """
        if html_data:
            soup = BeautifulSoup(html_data, 'lxml')
        else:
            soup = BeautifulSoup(self._last_response.get_data(), 'lxml')

        # Поиск сообщений о ошибках на странице
        error = soup.find('span', id='lblError')
        if error and error.text.strip() != '':
            raise ISBError(error.text.strip())

        # Парсим и возвращаем данные
        result_data_dict = []
        result_table = soup.find('table', id='pageBody_grid')
        if result_table:
            data_rows = result_table.find_all('tr')
            for row in data_rows[1:]:
                # npp, ic, c_n, v_number, v_brand, v_model, d_issue, c_from, c_to, status = [col.text.strip() for col in row.find_all('td')]
                # result_data_dict.append({
                #     'npp': npp,
                #     'insurance_company': ic,
                #     'contract_number': c_n,
                #     'contract_from': datetime.strptime(c_from, '%d.%m.%Y %H:%M:%S'),
                #     'contract_to': datetime.strptime(c_to, '%d.%m.%Y %H:%M:%S'),
                #     'd_issue': datetime.strptime(d_issue, '%d.%m.%Y %H:%M:%S'),
                #     'vehicle_number': v_number,
                #     'vehicle_brand': v_brand,
                #     'vehicle_model': v_model,
                #     'status': status
                # })

                cols = [col.text.strip() for col in row.find_all('td')]
                # for i, k in enumerate(cols):
                #     print i, k
                #
                # 0 1
                # 1 ATƏŞGAH SIĞORTA ŞİRKƏTİ ASC
                # 2 PAT1503254568
                # 3 10MH782
                # 4 125,00
                # 5 125,00
                # 6
                # 7 0
                # 8 28.02.2015 00:00:00
                # 9 27.02.2016 23:59:59

                result_data_dict.append({
                    'npp': cols[0],
                    'insurance_company': cols[1],
                    'contract_number': cols[2],
                    'contract_from': datetime.strptime(cols[8], '%d.%m.%Y %H:%M:%S'),
                    'contract_to': datetime.strptime(cols[9], '%d.%m.%Y %H:%M:%S'),
                })

        return result_data_dict

    def get_contracts_data(self, vehicle_number, try_cnt=3):
        """
        Receive data for vehicle number
        :param vehicle_number: vehicle registration number
        :return:
        """

        key = 'lib:isb_parser:%s' % vehicle_number
        result = cache.get(key)

        if result:
            return result

        cnt = 0
        while cnt < try_cnt:
            try:
                self._br.addheaders = [('User-agent', random.choice(USER_AGENTS))]

                if not self._last_response:
                    self._last_response = self._br.open(self._service_url, timeout=10)

                self._captcha_fp = '/tmp/captcha_%s.png' % hashlib.md5(vehicle_number).hexdigest()
                self._save_captcha(path=self._captcha_fp)

                img = Image.open(self._captcha_fp)
                capcha_str = pytesseract.image_to_string(img, lang='eng')

                os.remove(self._captcha_fp)

                self._br.select_form(nr=0)
                self._br['ctl00$pageBody$txtRegistrationNumber'] = vehicle_number
                self._br['ctl00$pageBody$txtCaptcha'] = capcha_str
                self._br.submit(nr=0)

                # print '%s -> %s' % (vehicle_number, cap)
                self._last_response = self._br.response()
                if self._last_response.code == 200:
                    result = self._parse_search_result()
                    cache.set(key, result, 60 * 60 * 3)  # 3 часа
                    return result

            except (ISBError, ):
                cnt += 1
                time.sleep(1)

    def test_tor_connection(self):
        print self._br.open('http://icanhazip.com').read()

u"""
from lib.isb_parser import ISBParser
isb_parser = ISBParser()
print isb_parser.get_contracts_data('10MH782')
"""
