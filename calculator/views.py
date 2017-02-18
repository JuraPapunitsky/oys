# coding=utf-8
import os
from uuid import uuid4
import hmac
import hashlib

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from suds import WebFault
from suds.client import Client

from lib.utils import send_mail
from lib.decorators import ajax_response

from calculator.constants import PRODUCTS, PRODUCT_COMPANIES, DELIVERY_REGION, OSAGO_INSURANT_FIELDS_MAP, OWNER_FIELDS_MAP, \
    AD1_FIELDS_MAP, AD2_FIELDS_MAP, DEFAULT_AXA_EXTENDED_REST, INSURANT_FIELDS_MAP, \
    DEFAULT_COUNTRY_OF_DEPARTURE, HEALTH_POLL_OPTIONS
from .utils import parse_get_tariff_response, get_tariff_matrix_html
from .forms import VehicleContract, PropertyContract, PropertyContractSave, TravelContract, HealthContract, OnlinePaymentForm
from . import models
from .operations import GetClassifier, BunchObject



class AjaxDataSourcesMixin(object):
    """
    Миксин источников данных AJAX и JSON
    """
    def call_method(self, request):
        # JSON data source functionality when calculator is called ?m=json&cl=<some_name>&.....
        # AJAX HTML data ?m=ajax&cl=<some_name>&.....
        method = request.GET.get('m', None)
        response_class = {'ajax': HttpResponse, 'json': JsonResponse}[method]
        collection_name = unicode(request.GET.get('cl'))
        collection_method = getattr(self, '%s_%s' % (method, collection_name[:30]), None)

        if collection_method:
            return response_class(collection_method(request))
        else:
            raise Http404()

    def get(self, request, *args, **kwargs):
        try:
            return self.call_method(request)
        except KeyError:
            # Попытка вызова несуществующей коллекции или недопустимого метода
            pass

        # Стандартная функциональность GET
        super_method = getattr(super(AjaxDataSourcesMixin, self), 'get', None)
        if super_method:
            return super_method(request, *args, **kwargs)
        else:
            raise Http404()

    def post(self, request, *args, **kwargs):
        try:
            return self.call_method(request)
        except KeyError:
            # Попытка вызова несуществующей коллекции или недопустимого метода
            pass

        # Стандартная функциональность POST
        super_method = getattr(super(AjaxDataSourcesMixin, self), 'post', None)
        if super_method:
            return super_method(request, *args, **kwargs)
        else:
            raise Http404()


class SoapClientMixin(object):
    u"""
    Миксин получения SOAP клиента
    """
    soap_client = None

    def _get_soap(self):
        """
        Ленивая инициализация SOAP клиента
        :return:
        """
        if self.soap_client is None:
            # Инициализация клиента SOAP
            self.soap_client = Client(settings.ASAN_SVC_URL, username=settings.ASAN_SVC_USER,
                                      password=settings.ASAN_SVC_PWD)
        return self.soap_client

    def _validate_partially(self, form_data, field_names):
        u"""
        Частичная валидация формы
        :param form_data: данные для формы
        :param field_names: список валидируемых полей
        :return:
        """
        form = self.form_class(form_data)

        # Если в форме есть какие-либо ошибки, то проверяем, есть ли ошибки по заполняемым полям {field_names}
        if not form.is_valid() and (set(field_names) & set(form.errors.keys())):
            return False
        else:
            return form.cleaned_data

    def _fill_from_form(self, obj, form_data, field_names, attr_name_map=None, **kwargs):
        u"""
        Заполнение аттирбутов объекта {obj} данными {form_data}, проведенными через валидацию в форме
        :param obj:
        :param form_data:
        :param field_names:
        :param kwargs:
        :return:
        """
        attr_name_map = {} if attr_name_map is None else attr_name_map

        # Если в форме есть какие-либо ошибки, то проверяем, есть ли ошибки по заполняемым полям {field_names}
        form_data = self._validate_partially(form_data, field_names)
        if not form_data:
            return False

        # Если нет ошибок по заполняемым полям {field_names}
        # Заполняем аттрибуты объекта из формы
        for fn in field_names:
            attr_name = attr_name_map.get(fn, fn)
            setattr(obj, attr_name, form_data.get(fn))

        # Заполняем аттрибуты объекта из именованых параметров
        for k, v in kwargs.items():
            setattr(obj, k, v)

        return True


class ProductCalculatorMixin(object):
    """
    Методы, общие для всех калькуляторов
    """

    def json_validate(self, request):
        u"""
        Валидация данных на форме калькулятора. Возвращает json ответ
        :param request:
        :return:
        """
        if request.method == 'POST':
            ct = self.form_class(request.POST)
        else:
            ct = self.form_class(request.GET)
        return {
            'has_errors': not ct.is_valid(),
            'errors': ct.errors.as_json()
        }


def ajax_calculator_reset(request):
    """

    :param request:
    :return:
    """
    return render_to_response('calculator/calculator_modal.html', context_instance=RequestContext(request))


class VehicleProductCalculator(AjaxDataSourcesMixin, SoapClientMixin, ProductCalculatorMixin, TemplateView):
    u"""
    Калькулятор продуктов по автострахованию
    """
    form_class = VehicleContract

    # Методы CBV

    def get_template_names(self):
        return [
            os.path.join('calculator', 'calculator_modal_vehicle.html'),
            os.path.join('calculator', 'calculator_modal_error.html'),  # fallback
            ]

    def get_context_data(self, **kwargs):
        context = kwargs

        context.update({
            'auto_regions': GetClassifier('docflow.AutoRegion').order_by('title').execute(),
            'countries': GetClassifier('docflow.Country').filter(id__in=(4, 60, 170, 213, 216)).execute(),
            'countries_more': GetClassifier('docflow.Country').exclude(id__in=(4, 60, 170, 213, 216)).execute(),
            'cities': GetClassifier('docflow.City').execute(),
            'cities_more': [],
            'delivery_cities': GetClassifier('docflow.City').filter(id__in=(1, 2)).execute(),
            'delivery_regions': [{'id': obj[0], 'title': obj[1]} for obj in DELIVERY_REGION],
            'ins_fields': OSAGO_INSURANT_FIELDS_MAP,
            'owner_fields': OWNER_FIELDS_MAP,
            'ad1_fields': AD1_FIELDS_MAP,
            'ad2_fields': AD2_FIELDS_MAP,
        })
        return super(VehicleProductCalculator, self).get_context_data(**context)

    # Источники данных

    def ajax_auto_mark(self, request):
        u"""
        Список марок ТС для калькулятора
        :param request:
        :return:
        """
        vt = request.GET.get('vt', None)
        if vt == '4':
            # AUDI, BMW, CHEVROLET, DAEWOO, FORD, HONDA, HYUNDAI, KIA, LADA, LIFAN, MERCEDES BENZ, NISSAN, OPEL, LEXUS,
            # RANGE ROVER, SKODA, TOYOTA, VOLKSWGEN, MG, PORSHE
            popular_mark_ids = (185, 200, 221, 229, 258, 278, 288, 308, 322, 332, 333, 360, 364, 379, 386, 399, 404,
                                463, 478, 500)
            vehicle_marks = GetClassifier('docflow.AutoMark').filter(id__in=popular_mark_ids).order_by('title').execute()
            vehicle_marks_other = GetClassifier('docflow.AutoMark').exclude(id__in=popular_mark_ids).order_by('title').execute()

        else:
            vehicle_marks = GetClassifier('docflow.AutoMark').filter(automodel__auto_type=vt).distinct('title').\
                order_by('title').execute()
            vehicle_marks_other = []

        params = {
            'step_title': _(u'Марка автомобиля'),
            'step_id': 'substep-2',
            'name': 'auto_mark',
            'objects': vehicle_marks,
            'objects_more': vehicle_marks_other
        }

        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_auto_model(self, request):
        vt = request.GET.get('vt', None)
        vb = request.GET.get('vb', None)
        if vt and vb:
            params = {
                'step_title': _(u'Модель автомобиля'),
                'step_id': 'substep-3',
                'name': 'auto_model',
                'objects': GetClassifier('docflow.AutoModel').filter(auto_type=vt, mark=vb).order_by('title').execute()
            }
        else:
            params = {
                'step_title': _(u'Модель автомобиля'),
                'step_id': 'substep-3',
                'name': 'auto_model',
                'objects': []
            }
        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_auto_engine_capacity(self, request):
        params = {
            'step_title': _(u'Объем двигателя'),
            'step_id': 'substep-4',
            'name': 'auto_engine_capacity',
            'objects': GetClassifier('docflow.LibTable2_44').execute()
        }
        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_cnt_seats(self, request):
        params = {
            'step_title': _(u'Количество мест'),
            'step_id': 'substep-4',
            'name': 'cnt_seats',
            'objects': GetClassifier('docflow.LibTable2_48').execute()
        }
        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_auto_payload(self, request):
        params = {
            'step_title': _(u'Максимальная грузоподъемность'),
            'step_id': 'substep-4',
            'name': 'auto_payload',
            'objects': GetClassifier('docflow.LibTable2_47').execute()
        }
        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_auto_year(self, request):
        years = GetClassifier('docflow.CreateYear').order_by('-title').execute()
        params = {
            'step_title': _(u'Год выпуска автомобиля'),
            'step_id': 'substep-5',
            'name': 'auto_createyear',
            'objects': years[:11],
            'objects_more': years[11:]
        }
        return render_to_string('calculator/steps/g_variative_substep.html', params)

    def ajax_precalculate(self, request):
        u"""
        Предварительный рассчет продуктов
        :param request:
        :return:
        """
        # Список продуктов с идентификаторами, названиями и минимальными расчетными стоимостями для
        # отображения на этапе 3
        if request.POST.get('auto_type') == '4':
            template_params = {
                'p%d' % k: {
                    'id': k,
                    'title': v['title'],
                    'description': v['description'],
                    'price': None
                } for k, v in PRODUCTS.items() if k in (2, 11, 12)
            }
        else:
            template_params = {'p2': {'id': 2, 'price': None}}
            template_params['p2'].update(PRODUCTS[2])

        # Формируем запрос на цены продуктов
        cl = self._get_soap()
        params = cl.factory.create('ns0:Params')
        if not self._fill_from_form(params, request.POST,
                                    ('auto_type', 'auto_engine_capacity', 'cnt_seats', 'auto_payload', 'auto_cost',
                                     'ins_person_pin'),
                                    {'p11_product_option': 'product_option'},
                                    transit=False, insurer_type=1, term_insurance=1,
                                    product_option='a-group-insurer-select',
                                    insurance_coverage=2000, accidents_quantity=1, cvi_extension_sum=None,
                                    accident_ins_sum=None, accident_ins_drivers=1, evacuation=False,
                                    additional_drivers=False):
            raise Exception

        products = cl.factory.create('integerArray')
        if request.POST.get('auto_type') == '4':
            products.integer.append(2)
            products.integer.append(11)
            products.integer.append(12)
        else:
            products.integer.append(2)

        # Определяем минимальные ценники по продуктам
        tariffs = cl.service.get_tariff(params=params, products=products)
        for t in tariffs.Tariff:
            product = template_params['p%d' % t.product]
            if not t.has_error and t.s_premium > 0 and (product['price'] is None or product['price'] > t.s_premium):
                product['price'] = t.s_premium

        # Прегенерация таблиц для следующего шага
        tariffs_dict = parse_get_tariff_response(tariffs)
        ins_companies_p2 = GetClassifier('docflow.InsCompany').filter(id__in=PRODUCT_COMPANIES[2]).order_by('title').\
            execute()
        ins_companies_p11 = GetClassifier('docflow.InsCompany').filter(id__in=PRODUCT_COMPANIES[11]).order_by('title').\
            execute()
        ins_companies_p12 = GetClassifier('docflow.InsCompany').filter(id__in=PRODUCT_COMPANIES[12]).order_by('title').\
            execute()

        template_params.update({
            'p2_preload': get_tariff_matrix_html((2, ), ins_companies_p2, tariffs_dict)
        })
        if request.POST.get('auto_type') == '4':
            template_params.update({
                'p11_preload': get_tariff_matrix_html((11, ), ins_companies_p11, tariffs_dict),
                'p12_preload': get_tariff_matrix_html((12, ), ins_companies_p12, tariffs_dict)
            })

        return render_to_string('calculator/steps/vehicle/step_3_content.html', template_params)

    def ajax_options(self, request):
        u"""
        Получение опций калькулятора, в зависимости от выбранного основного продукта для отображения 4 шага
        :param request: ожидается, что в GET передается переменная pr с идентификаторов основного продукта
        :return:
        """
        pr = request.GET.get('pr', None)  # основной выбранный продукт
        auto_type = request.GET.get('auto_type', None)  # тип авто
        params = {
            'product': pr,  # в шаблоне ожидается что значение - строка
            'auto_type': auto_type,
            'banks': GetClassifier('base.Bank').order_by('title').execute()
        }
        return render_to_string('calculator/steps/vehicle/step_4_options.html', params)

    def ajax_calculate(self, request):
        u"""
        Рассчет матрицы продуктов
        :param request: ожидается, что в GET передается переменная spr, где через запятую передаются идентификаторы
        проектов АСАН (2, 11, 12)
        :return:
        """
        selected_products = request.GET.get('spr', None)
        if selected_products:
            product_ids = map(int, list(set(selected_products.replace(' ', '').split(',')) & {'2', '11', '12'}))

            # Запрашиваем тарифы
            cl = self._get_soap()

            # Заполняем папраметры расчета из данных формы
            params = cl.factory.create('ns0:Params')
            if not self._fill_from_form(params, request.POST,
                                        ('auto_type', 'auto_engine_capacity', 'cnt_seats', 'auto_payload', 'auto_cost',
                                         'p11_product_option', 'insurance_coverage', 'accidents_quantity',
                                         'cvi_extension_sum', 'accident_ins_sum', 'accident_ins_drivers', 'evacuation',
                                         'additional_drivers', 'ins_person_pin'),
                                        {'p11_product_option': 'product_option'},
                                        transit=False, insurer_type=1, term_insurance=1):
                raise Exception

            # Список идентификаторов продуктов, для которых запрашиваются цены
            products = cl.factory.create('integerArray')
            for pid in product_ids:
                products.integer.append(pid)

            # Получаем тарифы по продуктам и раскладываем их в словарь
            # tariffs_dict = {<company_id> : {<product_id>: <value|None>, ...}, ...}
            tariffs = cl.service.get_tariff(params=params, products=products)
            tariffs_dict = parse_get_tariff_response(tariffs)
            ins_companies_list = []
            for pid in product_ids:
                ins_companies_list.extend(PRODUCT_COMPANIES[pid])

            ins_companies = GetClassifier('docflow.Inscompany').filter(id__in=ins_companies_list).order_by('title').\
                execute()
            return get_tariff_matrix_html(product_ids, ins_companies, tariffs_dict)

        return ''

    # Удаленные методы

    def json_issue(self, request):
        u"""
        Окончание оформления договора
        :param request:
        :return:
        """

        contract_form = self.form_class(request.POST)
        contract_valid = False
        contract_bonus_points = 0
        # Проверяется валидность данных по договорам
        if contract_form.is_valid():
            # Конструируем объект параметров для выхова процедуры выдачи договоров по автострахованию и заполняем
            # его данными из формы
            cl = self._get_soap()
            params = cl.factory.create('ns0:VehicleIssueParams')
            if not self._fill_from_form(params, request.POST,
                                        ('main_product', 'ins_person_pin', 'ins_person_lname',
                                         'ins_person_fname', 'ins_person_mname', 'ins_person_gender',
                                         'ins_person_birthday', 'ins_country', 'ins_city', 'ins_city_custom',
                                         'ins_address', 'ins_index', 'ins_street', 'ins_house', 'ins_apartment',
                                         'ins_phone', 'ins_email', 'delivery_type', 'delivery_date', 'delivery_time',
                                         'delivery_city', 'delivery_region', 'delivery_street', 'delivery_house',
                                         'delivery_apartment',
                                         'delivery_phone', 'delivery_comment', 'delivery_takeout', 'delivery_email',
                                         'payment_type', 'p2_selected', 'p11_selected', 'p12_selected', 'auto_type',
                                         'auto_mark', 'auto_model', 'auto_engine_capacity', 'auto_payload',
                                         'cnt_seats', 'auto_createyear', 'auto_vin', 'auto_engine', 'auto_chassis',
                                         'auto_number', 'auto_region', 'auto_cost', 'p2_inscompany', 'p11_inscompany',
                                         'p11_product_option', 'p11_beneficiary', 'p11_bank_beneficiary',
                                         'p12_inscompany', 'p12_beneficiary', 'p12_bank_beneficiary',
                                         'insurance_coverage', 'accidents_quantity', 'evacuation', 'cvi_extension_sum',
                                         'accident_ins_sum', 'accident_ins_drivers', 'additional_drivers',
                                         'additional_driver_2', 'ins_owner', 'owner_pin', 'owner_lname', 'owner_fname',
                                         'owner_mname', 'owner_gender', 'owner_birthday', 'owner_country', 'owner_city',
                                         'owner_city_custom', 'owner_address', 'owner_index', 'owner_street',
                                         'owner_house', 'owner_apartment', 'owner_phone', 'owner_email', 'ad1_pin',
                                         'ad1_lname', 'ad1_fname', 'ad1_mname', 'ad1_gender', 'ad1_birthday',
                                         'ad1_country', 'ad1_city', 'ad1_city_custom', 'ad1_address', 'ad1_index',
                                         'ad1_street', 'ad1_house', 'ad1_apartment', 'ad1_phone', 'ad1_email',
                                         'ad2_pin', 'ad2_lname', 'ad2_fname', 'ad2_mname', 'ad2_gender', 'ad2_birthday',
                                         'ad2_country', 'ad2_city', 'ad2_city_custom', 'ad2_address', 'ad2_index',
                                         'ad2_street', 'ad2_house', 'ad2_apartment', 'ad2_phone', 'ad2_email',
                                         'ateshgah_beshlik', 'ateshgah_icbariplus', 'ateshgah_superkasko'),
                                        {'p11_product_option': 'product_option'},
                                        transit=False, insurer_type=1, term_insurance=1):
                raise Exception

            try:
                response = cl.service.issue_vehicle_contracts(params)
                contract_form.instance.is_completed = True
                contract_form.instance.p2_id = response.p2_id if hasattr(response, 'p2_id') else None
                contract_form.instance.p11_id = response.p11_id if hasattr(response, 'p11_id') else None
                contract_form.instance.p12_id = response.p12_id if hasattr(response, 'p12_id') else None
                obj = contract_form.save()

                contract_bonus_points = 110
                contract_valid = True

            except WebFault as exc:
                from lib.utils import print_trace
                print_trace()
                contract_valid = False

            # Отправка уведомления администратору
            msg = render_to_string('calculator/email/vehicle_contract_created.html', {
                'asan_url': settings.ASAN_SVC_URL.replace('/site_integration/?wsdl', ''),
                'p2_number': contract_form.instance.p2_id,
                'p11_number': contract_form.instance.p11_id,
                'p12_number': contract_form.instance.p12_id
            })
            send_mail(u'Договор создан на сайте', msg, ['pavel.kuzko@gmail.com', 'dibrovsd@gmail.com'])

        return {
            'has_errors': not contract_valid,
            'premium_points': contract_bonus_points,
            'transaction_id': unicode(obj.id),
        }


class PropertyProductCalculator(AjaxDataSourcesMixin, SoapClientMixin, ProductCalculatorMixin, TemplateView):
    u"""
    Калькулятор продуктов по недвижимости
    """
    form_class = PropertyContract

    def get_template_names(self):
        return [
            os.path.join('calculator', 'calculator_modal_property.html'),
            os.path.join('calculator', 'calculator_modal_error.html'),  # fallback
            ]

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update({
            'using_methods': GetClassifier('docflow.LibTable3_16').order_by('title').execute(),
            'branches': GetClassifier('docflow.LibTable3_17').order_by('title').execute(),
            'countries': GetClassifier('docflow.Country').filter(id__in=(4, 60, 170, 213, 216)).execute(),
            'countries_more': GetClassifier('docflow.Country').exclude(id__in=(4, 60, 170, 213, 216)).execute(),
            'cities': GetClassifier('docflow.City').execute(),
            'cities_more': [],
            'delivery_cities': GetClassifier('docflow.City').filter(id__in=(1, 2)).execute(),
            'delivery_regions': [{'id': obj[0], 'title': obj[1]} for obj in DELIVERY_REGION],
            'ins_fields': INSURANT_FIELDS_MAP
        })

        return super(PropertyProductCalculator, self).get_context_data(**context)

    def ajax_precalculate(self, request):
        u"""
        Предварительный рассчет продуктов
        :param request:
        :return:
        """
        # Список продуктов с идентификаторами, названиями и минимальными расчетными стоимостями для
        # отображения на этапе 3
        template_params = {'p3': {'id': 3, 'price': None}}
        template_params['p3'].update(PRODUCTS[3])

        # Формируем запрос на цены продуктов
        cl = self._get_soap()
        params = cl.factory.create('ns0:Params')
        if not self._fill_from_form(params, request.POST, ('realty_type', 'city', 'branch', 's_insurance', 'franchise')):
            raise Exception

        products = cl.factory.create('integerArray')
        products.integer.append(3)

        # Определяем минимальные ценники по продуктам
        tariffs = cl.service.get_tariff(params=params, products=products)
        for t in tariffs.Tariff:
            product = template_params['p%d' % t.product]
            if not t.has_error and t.s_premium > 0 and (product['price'] is None or product['price'] > t.s_premium):
                product['price'] = t.s_premium

        # Прегенерация таблиц для следующего шага
        tariffs_dict = parse_get_tariff_response(tariffs)
        ins_companies = GetClassifier('docflow.InsCompany').filter(id__in=PRODUCT_COMPANIES[3]).order_by('title').\
            execute()
        template_params['p3_preload'] = get_tariff_matrix_html((3, ), ins_companies, tariffs_dict)

        return render_to_string('calculator/steps/property/step_3_content.html', template_params)

    def ajax_options(self, request):
        template_params = {
            'product': request.GET.get('pr'),
            'realty_type': request.GET.get('realty_type')
        }
        return render_to_string('calculator/steps/property/step_4_options.html', template_params)

    def ajax_calculate(self, request):
        u"""
        Рассчет матрицы продуктов
        :param request: ожидается, что в GET передается переменная spr, где через запятую передаются идентификаторы
        проектов АСАН (2, 11, 12)
        :return:
        """
        selected_products = request.GET.get('spr', None)
        if selected_products:
            product_ids = map(int, list(set(selected_products.replace(' ', '').split(',')) & {'3'}))

            # Запрашиваем тарифы
            cl = self._get_soap()

            # Заполняем папраметры расчета из данных формы
            params = cl.factory.create('ns0:Params')
            if not self._fill_from_form(params, request.POST,
                                        ('realty_type', 'city', 'branch', 's_insurance', 'franchise')):
                raise Exception

            # Список идентификаторов продуктов, для которых запрашиваются цены
            products = cl.factory.create('integerArray')
            for pid in product_ids:
                products.integer.append(pid)

            # Получаем тарифы по продуктам и раскладываем их в словарь
            # tariffs_dict = {<company_id> : {<product_id>: <value|None>, ...}, ...}
            tariffs = cl.service.get_tariff(params=params, products=products)
            tariffs_dict = parse_get_tariff_response(tariffs)
            ins_companies_list = []
            for pid in product_ids:
                ins_companies_list.extend(PRODUCT_COMPANIES[pid])

            ins_companies = GetClassifier('docflow.Inscompany').filter(id__in=ins_companies_list).order_by('title').execute()
            return get_tariff_matrix_html(product_ids, ins_companies, tariffs_dict)

        return ''

    def json_issue(self, request):
        u"""
        Окончание оформления договора
        :param request:
        :return:
        """
        obj_id = request.POST.get('id', None)
        if request.user.is_authenticated():
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client': request.user
            }
        else:
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client__isnull': True
            }

        obj = None
        if f_params['id'] and models.PropertyContract.objects.filter(**f_params).exists():
            obj = models.PropertyContract.objects.get(**f_params)

        contract_form = self.form_class(request.POST, instance=obj)
        contract_valid = False
        contract_bonus_points = 0
        # Проверяется валидность данных по договорам
        if contract_form.is_valid():
            # Конструируем объект параметров для выхова процедуры выдачи договоров по автострахованию и заполняем
            # его данными из формы
            cl = self._get_soap()
            params = cl.factory.create('ns0:PropertyIssueParams')
            if not self._fill_from_form(params, request.POST,
                                        ('main_product', 'd_start', 'ins_person_pin', 'ins_person_lname',
                                         'ins_person_fname', 'ins_person_mname', 'ins_person_gender',
                                         'ins_person_birthday', 'ins_country', 'ins_city', 'ins_city_custom',
                                         'ins_address', 'ins_index', 'ins_street', 'ins_house', 'ins_apartment',
                                         'ins_phone', 'ins_email', 'delivery_type', 'delivery_date', 'delivery_time',
                                         'delivery_city', 'delivery_region', 'delivery_street', 'delivery_house',
                                         'delivery_apartment',
                                         'delivery_phone', 'delivery_comment', 'delivery_takeout', 'delivery_email',
                                         'payment_type', 'p3_selected', 'p3_inscompany', 'realty_type', 'city',
                                         'branch', 's_insurance', 'franchise', 'using_method', 'address', 'index',
                                         'n_reestr', 'document_reason'), None, insurer_type=1, term_insurance=1):
                raise Exception

            try:
                response = cl.service.issue_property_contracts(params)
                contract_form.instance.is_completed = True
                # Привязка польдователя если он прошел аутентификацию
                if request.user.is_authenticated():
                    contract_form.instance.client = request.user
                contract_form.instance.p3_id = response.p3_id if hasattr(response, 'p3_id') else None
                contract_form.save()
                contract_bonus_points = 110
                contract_valid = True

            except WebFault as exc:
                contract_valid = False

            # Отправка уведомления администратору
            msg = render_to_string('calculator/email/property_contract_created.html', {
                'asan_url': settings.ASAN_SVC_URL.replace('/site_integration/?wsdl', ''),
                'p3_number': contract_form.instance.p3_id,
            })
            send_mail(u'Договор создан на сайте', msg, ['pavel.kuzko@gmail.com', ])

        return {
            'has_errors': not contract_valid,
            'premium_points': contract_bonus_points
        }

    def json_restore(self, request):
        u"""
        Получение данных для восстановления расчета в калькуляторе
        :param request:
        :return:
        """
        obj_id = request.GET.get('id')
        if request.user.is_authenticated():
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client': request.user
            }
        else:
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client__isnull': True
            }

        if f_params['id'] and models.PropertyContract.objects.filter(**f_params).exists():
            obj = models.PropertyContract.objects.get(**f_params)
            d = {k: getattr(obj, k) for k in ('id', 'realty_type', 'city', 's_insurance', 'franchise', 'branch',
                                              'main_product', 'p3_inscompany', 'n_reestr', 'document_reason',
                                              'using_method', 'address', 'index', 'ins_country', 'ins_city',
                                              'ins_index', 'ins_street', 'ins_house', 'ins_apartment', 'ins_person_pin',
                                              'ins_person_fname', 'ins_person_lname', 'ins_person_mname',
                                              'ins_person_gender', 'ins_person_birthday', 'ins_phone', 'ins_email',
                                              'delivery_region', 'delivery_time')}
            d['id'] = str(d['id'])  # приведение к строке, т.к. UUID не сериализуется
            d['ins_person_birthday'] = d['ins_person_birthday'].strftime('%d.%m.%Y') if d['ins_person_birthday'] else ''
            return d
        return {
            'id': ''
        }

    def json_save(self, request):
        u"""
        Сохранение данных калькулятора без валидации
        :param request:
        :return:
        """
        obj_id = request.POST.get('id', None)
        if request.user.is_authenticated():
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client': request.user
            }
        else:
            f_params = {
                'id': obj_id,
                'is_completed': False,
                'client__isnull': True
            }

        obj = None
        if f_params['id'] and models.PropertyContract.objects.filter(**f_params).exists():
            obj = models.PropertyContract.objects.get(**f_params)

        contract_form = PropertyContractSave(request.POST, instance=obj)

        # Привязка польдователя если он прошел аутентификацию
        if request.user.is_authenticated():
            contract_form.instance.client = request.user

        contract_form.save()

        return {
            'status': 'success',
            'id': str(contract_form.instance.id)
        }


class TravelProductCalculator(AjaxDataSourcesMixin, SoapClientMixin, ProductCalculatorMixin, TemplateView):
    u"""
    Калькулятор продуктов по путешествий
    """
    form_class = TravelContract

    def get_template_names(self):
        return [
            os.path.join('calculator', 'calculator_modal_travel.html'),
            os.path.join('calculator', 'calculator_modal_error.html'),  # fallback
            ]

    def get_context_data(self, **kwargs):
        context = kwargs

        # Страховые суммы по ВЗР
        ins_values = GetClassifier('docflow.LibTable4_42').filter(deleted=False).order_by('title').execute()
        ins_values.sort(key=lambda v: int(v.title.replace(' ', '')))

        context.update({
            'ins_values': ins_values,
            'embassies': GetClassifier('docflow.LibTable4_68').order_by('title').execute(),
            'travel_countries': GetClassifier('docflow.Country').exclude(id__in=(14, 240, 258)).order_by('title').execute(),
            'countries': GetClassifier('docflow.Country').filter(id__in=(4, 60, 170, 213, 216)).order_by('title').execute(),
            'countries_more': GetClassifier('docflow.Country').exclude(id__in=(4, 60, 170, 213, 216)).order_by('title').execute(),
            'cities': GetClassifier('docflow.City').execute(),
            'cities_more': [],
            'delivery_cities': GetClassifier('docflow.City').filter(id__in=(1, 2)).execute(),
            'delivery_regions': [{'id': obj[0], 'title': obj[1]} for obj in DELIVERY_REGION],
            'ins_fields': INSURANT_FIELDS_MAP
        })

        return super(TravelProductCalculator, self).get_context_data(**context)

    def json_shengen_add(self, request):
        u"""
        Получение количества застрахованных дней и расширения засчет Шенгена
        :param request:
        :return:
        """
        cl = self._get_soap()
        countries = ','.join(request.POST.getlist('countries[]'))
        result = cl.service.get_travel_shengen_add(countries)
        return {
            'shengen_add': result if result else 0
        }

    def ajax_precalculate(self, request):
        u"""
        Предварительный расчет продуктов
        :param request:
        :return:
        """
        # Список продуктов с идентификаторами, названиями и минимальными расчетными стоимостями для
        # отображения на этапе 3
        template_params = {'p4': {'id': 4, 'price': None}}
        template_params['p4'].update(PRODUCTS[4])

        # Формируем запрос на цены продуктов
        cl = self._get_soap()
        params = cl.factory.create('ns0:Params')

        form_data = self._validate_partially(request.POST, ('traveller_birthday', 'rest_type'))
        if not form_data:
            raise Exception

        countries = cl.factory.create('integerArray')
        countries.integer.extend(map(int, request.POST.getlist('countries[]')))
        params.countries = countries

        birthdates = cl.factory.create('dateArray')
        birthdates.date.append(form_data.get('traveller_birthday'))
        params.birthdates = birthdates

        rest_type = form_data['rest_type']
        if not self._fill_from_form(params, request.POST, ('rest_type', 'd_start', 'd_end', 'insured_days', 'rest_term_year'), {},
                                    currency=2, ins_value=2, embassy='', risk_group=1,
                                    departure_type=1, rest_type_extended=DEFAULT_AXA_EXTENDED_REST[rest_type]):
            raise Exception

        products = cl.factory.create('integerArray')
        products.integer.append(4)

        # Определяем минимальные ценники по продуктам
        tariffs = cl.service.get_tariff(params=params, products=products)
        for t in tariffs.Tariff:
            product = template_params['p%d' % t.product]
            if not t.has_error and t.s_premium > 0 and (product['price'] is None or product['price'] > t.s_premium):
                product['price'] = t.s_premium

        # Прегенерация таблиц для следующего шага
        tariffs_dict = parse_get_tariff_response(tariffs)
        ins_companies = GetClassifier('docflow.InsCompany').filter(id__in=PRODUCT_COMPANIES[4]).order_by('title').\
            execute()
        template_params['p4_preload'] = get_tariff_matrix_html((4, ), ins_companies, tariffs_dict)

        return render_to_string('calculator/steps/travel/step_3_content.html', template_params)

    def ajax_calculate(self, request):
        u"""
        Рассчет матрицы продуктов
        :param request: ожидается, что в GET передается переменная spr, где через запятую передаются идентификаторы
        проектов АСАН
        :return:
        """
        selected_products = request.GET.get('spr', None)
        if selected_products:
            product_ids = map(int, list(set(selected_products.replace(' ', '').split(',')) & {'4'}))

            # Запрашиваем тарифы
            cl = self._get_soap()
            params = cl.factory.create('ns0:Params')

            form_data = self._validate_partially(request.POST, ('traveller_birthday', 'rest_type'))
            if not form_data:
                raise Exception

            countries = cl.factory.create('integerArray')
            countries.integer.extend(map(int, request.POST.getlist('countries[]')))
            params.countries = countries

            birthdates = cl.factory.create('dateArray')
            birthdates.date.append(form_data.get('traveller_birthday'))
            params.birthdates = birthdates

            rest_type = form_data['rest_type']
            if not self._fill_from_form(params, request.POST, ('rest_type', 'd_start', 'd_end', 'currency', 'insured_days',
                                                               'ins_value', 'risk_group', 'departure_type', 'rest_term_year'), {},
                                        embassy='', rest_type_extended=DEFAULT_AXA_EXTENDED_REST[rest_type]):
                raise Exception

            print params

            # Список идентификаторов продуктов, для которых запрашиваются цены
            products = cl.factory.create('integerArray')
            for pid in product_ids:
                products.integer.append(pid)

            # Получаем тарифы по продуктам и раскладываем их в словарь
            # tariffs_dict = {<company_id> : {<product_id>: <value|None>, ...}, ...}
            tariffs = cl.service.get_tariff(params=params, products=products)
            tariffs_dict = parse_get_tariff_response(tariffs)
            ins_companies_list = []
            for pid in product_ids:
                ins_companies_list.extend(PRODUCT_COMPANIES[pid])

            ins_companies = GetClassifier('docflow.Inscompany').filter(id__in=ins_companies_list).order_by('title').execute()
            return get_tariff_matrix_html(product_ids, ins_companies, tariffs_dict)

        return ''

    def json_issue(self, request):
        u"""
        Окончание оформления договора
        :param request:
        :return:
        """
        obj_id = request.POST.get('id', None)
        if request.user.is_authenticated():
            f_params = {'id': obj_id, 'is_completed': False, 'client': request.user}
        else:
            f_params = {'id': obj_id, 'is_completed': False, 'client__isnull': True}

        obj = None
        if f_params['id'] and models.TravelContract.objects.filter(**f_params).exists():
            obj = models.TravelContract.objects.get(**f_params)

        contract_form = self.form_class(request.POST, instance=obj)
        contract_valid = False
        contract_bonus_points = 0

        # Проверяется валидность данных по договорам
        if contract_form.is_valid():
            rest_type_extended = DEFAULT_AXA_EXTENDED_REST[contract_form.cleaned_data['rest_type']]
            # Конструируем объект параметров для выхова процедуры выдачи договоров по автострахованию и заполняем
            # его данными из формы
            cl = self._get_soap()
            params = cl.factory.create('ns0:TravelIssueParams')
            if not self._fill_from_form(params, request.POST,
                                        ('main_product', 'ins_person_pin', 'ins_person_lname',
                                         'ins_person_fname', 'ins_person_mname', 'ins_person_gender',
                                         'ins_person_birthday', 'ins_country', 'ins_city', 'ins_city_custom',
                                         'ins_address', 'ins_index', 'ins_street', 'ins_house', 'ins_apartment',
                                         'ins_phone', 'ins_email', 'delivery_type', 'delivery_date', 'delivery_time',
                                         'delivery_city', 'delivery_region', 'delivery_street', 'delivery_house',
                                         'delivery_apartment', 'delivery_phone', 'delivery_comment', 'delivery_takeout',
                                         'delivery_email', 'payment_type', 'p4_selected', 'p4_inscompany', 'embassy',
                                         'rest_type', 'd_start', 'd_end', 'currency', 'insured_days',
                                         'ins_value', 'risk_group', 'departure_type', 'rest_term_year',
                                         'traveller_first_name', 'traveller_last_name', 'traveller_middle_name',
                                         'traveller_n_passport', 'traveller_gender', 'traveller_birthday',
                                         'traveller_address', 'traveller_pin', 'traveller_city'), None,
                                        insurer_type=1, rest_type_extended=rest_type_extended,
                                        country_of_departure=DEFAULT_COUNTRY_OF_DEPARTURE):
                raise Exception

            countries_list = request.POST.getlist('countries[]')
            countries = cl.factory.create('integerArray')
            countries.integer.extend(map(int, countries_list))
            params.countries = countries

            try:
                response = cl.service.issue_travel_contracts(params)

                contract = contract_form.instance
                contract.is_completed = True
                contract.countries = ','.join(countries_list)
                contract.country_of_departure = DEFAULT_COUNTRY_OF_DEPARTURE
                contract.rest_type_extended = rest_type_extended
                contract.p4_id = response.p4_id if hasattr(response, 'p4_id') else None

                # Привязка польдователя если он прошел аутентификацию
                if request.user.is_authenticated():
                    contract.client = request.user

                contract_form.save()
                contract_bonus_points = 0
                contract_valid = True

            except WebFault:
                contract_valid = False

            # Отправка уведомления администратору
            msg = render_to_string('calculator/email/travel_contract_created.html', {
                'asan_url': settings.ASAN_SVC_URL.replace('/site_integration/?wsdl', ''),
                'p4_number': contract_form.instance.p4_id,
            })
            send_mail(u'Договор создан на сайте', msg, ['pavel.kuzko@gmail.com', ])

        return {
            'has_errors': not contract_valid,
            'premium_points': contract_bonus_points
        }


class HealthProductCalculator(AjaxDataSourcesMixin, SoapClientMixin, ProductCalculatorMixin, TemplateView):
    u"""
    Калькулятор продуктов по страхованию здоровья
    """
    form_class = HealthContract

    def get_template_names(self):
        return [
            os.path.join('calculator', 'calculator_modal_health.html'),
            os.path.join('calculator', 'calculator_modal_error.html'),  # fallback
            ]

    def get_context_data(self, **kwargs):
        context = kwargs

        context.update({
            'health_poll': [BunchObject(**kwargs) for kwargs in HEALTH_POLL_OPTIONS],
            'countries': GetClassifier('docflow.Country').filter(id__in=(4, 60, 170, 213, 216)).order_by('title').execute(),
            'countries_more': GetClassifier('docflow.Country').exclude(id__in=(4, 60, 170, 213, 216)).order_by('title').execute(),
            'cities': GetClassifier('docflow.City').execute(),
            'cities_more': [],
            'delivery_cities': GetClassifier('docflow.City').filter(id__in=(1, 2)).execute(),
            'delivery_regions': [{'id': obj[0], 'title': obj[1]} for obj in DELIVERY_REGION],
            'ins_fields': INSURANT_FIELDS_MAP
        })

        return super(HealthProductCalculator, self).get_context_data(**context)

    def ajax_precalculate(self, request):
        u"""
        Предварительный расчет стоимостей страховых продуктов
        :param request:
        :return:
        """
        # Формируем запрос на цены продуктов
        cl = self._get_soap()
        params = cl.factory.create('ns0:Params')
        params_ins_products = cl.factory.create('integerArray')

        # Список продуктов доступных клиенту определяется по дате рождения: от 0 до 14 - REFUND, от 14 до 55 Urgent Care
        # и Program 69, старше 55 - продуктов нет
        insured_birthday = parse(request.POST.get('insured_birthday'), dayfirst=True)
        now = timezone.now().date()
        insured_full_years = relativedelta(now, insured_birthday).years
        if 0 <= insured_full_years <= 14:
            ins_products = ('9_2', )
            params_ins_products.integer.append(2)
        elif 14 < insured_full_years < 55:
            ins_products = ('9_1', '9_3')
            params_ins_products.integer.append(1)
            params_ins_products.integer.append(3)
        else:
            ins_products = ()
        params.ins_products = params_ins_products

        template_params = {
            'ins_products': ins_products
        }

        # Если есть страховые продукты для клиента
        if ins_products:

            # Заполняем исходные данные для страховых продуктов
            for p_id in ins_products:
                template_params['p%s' % p_id] = {'id': p_id, 'price': None, 'error': ''}
                template_params['p%s' % p_id].update(PRODUCTS[p_id] if p_id in PRODUCTS else {})

            # Заполняем параметры предварительного расчета страховых продуктов
            if not self._fill_from_form(params, request.POST, ('insured_birthday', ), {},
                                        deductible=25, massage=False, vac=False,
                                        health_poll=','.join(request.POST.getlist('health_poll[]'))):
                raise Exception

            products = cl.factory.create('integerArray')
            products.integer.append(9)

            # Определяем минимальные ценники по продуктам и актуализируем данные в словаре для рендеринга шаблона
            tariffs = cl.service.get_tariff(params=params, products=products)
            for t in tariffs.Tariff:
                product = template_params['p%s' % t.sub_product]

                if t.has_error:
                    product['error'] = t.message
                elif t.s_premium > 0 and (product['price'] is None or product['price'] > t.s_premium):
                    product['price'] = t.s_premium

        return render_to_string('calculator/steps/health/step_3_content.html', template_params)

    def ajax_options(self, request):
        u"""
        Загрузка доступных опций для 4 шага
        :param request:
        :return:
        """
        product = request.GET.get('pr').replace('9_', '')
        template_params = {
            'product': product
        }
        return render_to_string('calculator/steps/health/step_4_options.html', template_params)

    def json_products(self, request):
        u"""
        Расчет стоимости продуктов
        :param request:
        :return:
        """
        cl = self._get_soap()
        params = cl.factory.create('ns0:Params')

        # Расчет всегда производим по всем имеющимся в системе продуктам
        params_ins_products = cl.factory.create('integerArray')
        for i in xrange(1, 6):
            params_ins_products.integer.append(i)
        params.ins_products = params_ins_products

        if not self._fill_from_form(params, request.POST, ('insured_birthday', 'deductible', 'massage', 'vac'), {},
                                    health_poll=','.join(request.POST.getlist('health_poll[]'))):
            raise Exception

        products = cl.factory.create('integerArray')
        products.integer.append(9)
        tariffs = cl.service.get_tariff(params=params, products=products)

        result = {}
        for t in tariffs.Tariff:
            result[t.sub_product] = {'price': 0.0 if t.has_error else t.s_premium,
                                     'error': t.message if t.has_error else ''}
        return result

    def json_issue(self, request):
        u"""
        Окончание оформления договора
        :param request:
        :return:
        """
        obj_id = request.POST.get('id', None)
        if request.user.is_authenticated():
            f_params = {'id': obj_id, 'is_completed': False, 'client': request.user}
        else:
            f_params = {'id': obj_id, 'is_completed': False, 'client__isnull': True}

        obj = None
        if f_params['id'] and models.HealthContract.objects.filter(**f_params).exists():
            obj = models.HealthContract.objects.get(**f_params)

        contract_form = self.form_class(request.POST, instance=obj)
        contract_valid = False
        contract_bonus_points = 0

        # Проверяется валидность данных по договорам
        if contract_form.is_valid():
            # Конструируем объект параметров для выхова процедуры выдачи договоров по автострахованию и заполняем
            # его данными из формы
            cl = self._get_soap()
            params = cl.factory.create('ns0:HealthIssueParams')
            if not self._fill_from_form(params, request.POST,
                                        ('main_product', 'ins_person_pin', 'ins_person_lname',
                                         'ins_person_fname', 'ins_person_mname', 'ins_person_gender',
                                         'ins_person_birthday', 'ins_country', 'ins_city', 'ins_city_custom',
                                         'ins_address', 'ins_index', 'ins_street', 'ins_house', 'ins_apartment',
                                         'ins_phone', 'ins_email', 'delivery_type', 'delivery_date', 'delivery_time',
                                         'delivery_city', 'delivery_region', 'delivery_street', 'delivery_house',
                                         'delivery_apartment', 'delivery_phone', 'delivery_comment', 'delivery_takeout',
                                         'delivery_email', 'payment_type', 'p9_1_selected', 'p9_2_selected',
                                         'p9_3_selected', 'refund_vip', 'program69_extended', 'vac', 'massage',
                                         'insured_lname', 'insured_fname', 'insured_mname', 'insured_birthday',
                                         'deductible', 'p9_1_payment', 'p9_2_payment', 'p9_3_payment'), None,
                                        insurer_type=1):
                raise Exception

            health_poll_list = request.POST.getlist('health_poll[]')
            health_poll = cl.factory.create('integerArray')
            health_poll.integer.extend(map(int, health_poll_list))
            params.health_poll = health_poll

            try:
                response = cl.service.issue_health_contracts(params)

                contract = contract_form.instance
                contract.is_completed = True
                contract.health_poll = ','.join(health_poll_list)
                contract.p9_1_id = response.p9_1_id if hasattr(response, 'p9_1_id') else None
                contract.p9_2_id = response.p9_2_id if hasattr(response, 'p9_2_id') else None
                contract.p9_3_id = response.p9_3_id if hasattr(response, 'p9_3_id') else None

                # Привязка польдователя если он прошел аутентификацию
                if request.user.is_authenticated():
                    contract.client = request.user

                contract_form.save()
                contract_bonus_points = 0
                contract_valid = True

            except WebFault:
                contract_valid = False

            # Отправка уведомления администратору
            msg = render_to_string('calculator/email/health_contract_created.html', {
                'asan_url': settings.ASAN_SVC_URL.replace('/site_integration/?wsdl', ''),
                'p9_1_id': contract_form.instance.p9_1_id,
                'p9_2_id': contract_form.instance.p9_2_id,
                'p9_3_id': contract_form.instance.p9_3_id,
            })
            send_mail(u'Договор создан на сайте', msg, ['pavel.kuzko@gmail.com', ])

        return {
            'has_errors': not contract_valid,
            'premium_points': contract_bonus_points
        }


class OnlinePaymentFormView(TemplateView):
    u""" Форма online-оплаты. Запрашивается через ajax """

    template_name = 'calculator/online_payment_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(OnlinePaymentFormView, self).get_context_data(**kwargs)
        request = self.request
        now = timezone.now()
        nonce = uuid4().get_hex()

        data = (
            ('AMOUNT', request.GET['amount']),
            ('CURRENCY', 'AZN'),
            ('ORDER', request.GET['order']),
            ('DESC', 'INSURANCE_PAYMENT'),
            ('MERCH_NAME', 'OYSB'),
            ('MERCH_URL', 'www.oys.az'),
            ('TERMINAL', '64646464'),
            ('EMAIL', 'info@oys.az'),
            ('TRTYPE', '1'),
            ('COUNTRY', 'AZ'),
            ('MERCH_GMT', '+4'),
            ('TIMESTAMP', now.strftime('%Y%m%d%H%M%S')),
            ('NONCE', nonce),
            ('BACKREF', 'www.oys.az'),
        )
        initial = dict(data)

        # Собираем подпись
        sign_items = []
        for k, v in data:
            sign_items.append(u'%s%s' % (len(v), v))
        p_sign = u''.join(sign_items)

        # Добавим к параметрам
        key = '*******'
        initial['P_SIGN'] = hmac.new(key, p_sign, hashlib.sha1).hexdigest()

        form = OnlinePaymentForm(initial=initial)
        ctx['form'] = form
        ctx['amount'] = request.GET['amount']

        return ctx


@ajax_response
def check_payment(request, product, key):
    if product == 'vehicle':
        model = models.VehicleContract

    try:
        obj = model.objects.get(pk=key)
        if obj.s_payment and obj.s_premium == obj.s_payment:
            return True
        else:
            return False

    except model.DoesNotExist:
        return False
