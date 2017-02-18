# coding=utf-8
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from calculator.constants import DELIVERY_INTERVALS, DELIVERY_REGION
from calculator.operations import GetClassifier


PERSON_GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),
)

VEHICLE_TRANSIT_CHOICES = (
    (0, _('No')),
    (1, _('Yes')),
)

PAYMENT_TYPES = (
    ('cash', _('Cash')),
    ('epay', _('Online payment'))
)


def get_choices(name):
    if name:
        return [(obj.id, _(obj.title)) for obj in GetClassifier(name).execute()]

    return [('', '-' * 9)]


class ContractCalculationAbstract(models.Model):
    u"""
    Абстрактный класс с типовыми данными по договору
    """

    # Системные
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, editable=False,
                               verbose_name=_('client'))
    d_create = models.DateTimeField(_('creation date'), auto_now_add=True, editable=False, db_index=True)
    # Признак того, что договор оформлен в калькуляторе до конца (проставляется при окончании процесса оформления
    # в калькуляторе)
    is_completed = models.BooleanField(_('completed'), default=False, editable=False, db_index=True)
    # Признак того, что договор выпущен на стороне брокера (должен проставляться извне)
    is_issued = models.BooleanField(_('issued'), default=False, editable=False, db_index=True)

    # Состояние интерфейса процесса
    step = models.CharField(_('calculator step'), max_length=50)
    substep = models.CharField(_('calculator sub step'), max_length=50)
    layer = models.CharField(_('calculator layer'), max_length=50)

    # Общие данные о текущем расчете, условия договора
    main_product = models.CharField(_('main product ID'), max_length=10, null=True, blank=True)
    main_product_text = models.CharField(_('main product title'), max_length=100, null=True, blank=True)

    # Условия страхования
    d_start = models.DateField(_('contract start date'), null=True, blank=True)
    term_insurance = models.PositiveSmallIntegerField(_('term insurance'), null=True, blank=True)

    # Страхователь
    ins_person_pin = models.CharField(_('PIN'), max_length=9, null=True, blank=True)
    ins_person_lname = models.CharField(_('last name'), max_length=50, null=True, blank=True)
    ins_person_fname = models.CharField(_('first name'), max_length=50, null=True, blank=True)
    ins_person_mname = models.CharField(_('middle name'), max_length=50, null=True, blank=True)
    ins_person_gender = models.PositiveSmallIntegerField(_('gender'), choices=PERSON_GENDER_CHOICES, default=1)
    ins_person_birthday = models.DateField(_('birthday'), null=True, blank=True)
    ins_country = models.PositiveIntegerField(_('country'), null=True, blank=True)

    ins_index = models.CharField(_('postal index (ZIP)'), max_length=6, null=True, blank=True)
    ins_city = models.PositiveIntegerField(_('city'), null=True, blank=True)
    ins_city_custom = models.CharField(_('city (custom)'), max_length=50, null=True, blank=True)
    ins_address = models.CharField(_('address'), max_length=70, null=True, blank=True)
    ins_street = models.CharField(_('street'), max_length=50, null=True, blank=True)
    ins_house = models.CharField(_('house'), max_length=10, null=True, blank=True)
    ins_apartment = models.CharField(_('apartment'), max_length=10, null=True, blank=True)
    ins_phone = models.CharField(_('phone'), max_length=12, null=True, blank=True)
    ins_email = models.EmailField(_('email'), null=True, blank=True)

    # Доставка и оплата
    delivery_type = models.CharField(_('delivery type'), max_length=10, null=True, blank=True)
    delivery_date = models.DateField(_('delivery date'), null=True, blank=True)
    delivery_time = models.IntegerField(_('delivery time interval'), null=True, blank=True, choices=DELIVERY_INTERVALS)
    delivery_city = models.PositiveIntegerField(_('city'), null=True, blank=True)
    delivery_region = models.CharField(_('region'), max_length=50, blank=True, null=True, choices=DELIVERY_REGION)
    delivery_street = models.CharField(_('street'), max_length=50, null=True, blank=True)
    delivery_house = models.CharField(_('house'), max_length=10, null=True, blank=True)
    delivery_apartment = models.CharField(_('apartment'), max_length=10, null=True, blank=True)
    delivery_phone = models.CharField(_('phone'), max_length=12, null=True, blank=True)
    delivery_comment = models.TextField(_('comments'), null=True, blank=True)
    delivery_takeout = models.IntegerField(_('takeout point'), null=True, blank=True)
    delivery_email = models.EmailField(_('delivery email'), null=True, blank=True)

    # Платежи
    payment_type = models.CharField(_('payment type'), max_length=10, null=True, blank=True, choices=PAYMENT_TYPES)
    s_premium = models.FloatField(null=True)

    # Онлайн-оплата
    d_payment = models.DateTimeField(null=True)
    s_payment = models.FloatField(null=True)

    class Meta:
        app_label = 'calculator'
        abstract = True


class VehicleContract(ContractCalculationAbstract):
    u"""
    Комплексный договор по страхованию ТС (ОСАГО, Уверенный водитель, Простое КАСКО)
    """

    # Общие данные о текущем расчете, условия договора
    p2_selected = models.BooleanField(_('product 2 selected'), default=False)
    p11_selected = models.BooleanField(_('product 11 selected'), default=False)
    p12_selected = models.BooleanField(_('product 12 selected'), default=False)
    p2_id = models.PositiveIntegerField(_('p2 document id'), null=True, blank=True)
    p11_id = models.PositiveIntegerField(_('p11 document id'), null=True, blank=True)
    p12_id = models.PositiveIntegerField(_('p12 document id'), null=True, blank=True)

    # Страхователь наследуется

    # Автомобиль
    auto_type = models.PositiveIntegerField(_('vehicle type'))
    auto_mark = models.PositiveIntegerField(_('vehicle mark'))
    auto_model = models.PositiveIntegerField(_('vehicle model'))
    auto_engine_capacity = models.PositiveIntegerField(_('vehicle engine capacity'), null=True, blank=True)
    auto_payload = models.PositiveIntegerField(_('vehicle payload'), null=True, blank=True)
    cnt_seats = models.PositiveIntegerField(_('vehicle seats'), null=True, blank=True)
    auto_createyear = models.PositiveIntegerField(_('vehicle creation year'), null=True, blank=True)
    auto_vin = models.CharField('VIN', max_length=17, null=True, blank=True)
    auto_engine = models.CharField('EIN', max_length=17, null=True, blank=True)
    auto_chassis = models.CharField('CIN', max_length=17, null=True, blank=True)
    auto_number = models.CharField(_('vehicle registration number'), max_length=12)
    auto_region = models.PositiveIntegerField(_('vehicle registration region'))
    auto_cost = models.PositiveIntegerField(_('vehicle cost'))

    # Продукт ОСАГО
    p2_inscompany = models.PositiveSmallIntegerField(_('insurance company'), null=True, blank=True)
    ateshgah_beshlik = models.BooleanField(_('ateshgah beshlik'), default=False)
    ateshgah_icbariplus = models.BooleanField(_('ateshgah icbariplus'), default=False)
    ateshgah_superkasko = models.BooleanField(_('ateshgah superkasko'), default=False)

    # Продукт Уверенный водитель
    p11_inscompany = models.PositiveSmallIntegerField(_('insurance company'), null=True, blank=True)
    p11_product_option = models.CharField(_('station selection'), max_length=50, null=True, blank=True)
    p11_beneficiary = models.CharField(_('beneficiary'), max_length=10, null=True, blank=True)
    p11_bank_beneficiary = models.PositiveSmallIntegerField(_('bank'), null=True, blank=True)

    # Продукт Простое КАСКО
    p12_inscompany = models.PositiveIntegerField(_('insurance company'), null=True, blank=True)
    p12_beneficiary = models.CharField(_('beneficiary'), max_length=10, null=True, blank=True)
    p12_bank_beneficiary = models.PositiveIntegerField(_('bank'), null=True, blank=True)
    insurance_coverage = models.PositiveIntegerField(_('insurance sum'), null=True, blank=True)
    accidents_quantity = models.PositiveIntegerField(_('accidents quantity'), null=True, blank=True)
    evacuation = models.BooleanField(_('evacuation'), default=False)
    cvi_extension_sum = models.PositiveIntegerField(_('cvi extension sum'), null=True, blank=True)
    accident_ins_sum = models.PositiveIntegerField(_('accident insurance sum'), null=True, blank=True)
    accident_ins_drivers = models.PositiveSmallIntegerField(_('accident insurance drivers'), null=True, blank=True)
    additional_drivers = models.BooleanField(_('additional drivers'), default=False)
    additional_driver_2 = models.BooleanField(_('second additional driver'), default=False)

    # Владелец ТС
    ins_owner = models.BooleanField(_('insurant is vehicle owner'), default=True)
    owner_pin = models.CharField(_('PIN'), max_length=9, null=True, blank=True)
    owner_lname = models.CharField(_('last name'), max_length=50, null=True, blank=True)
    owner_fname = models.CharField(_('first name'), max_length=50, null=True, blank=True)
    owner_mname = models.CharField(_('middle name'), max_length=50, null=True, blank=True)
    owner_gender = models.PositiveSmallIntegerField(_('gender'), null=True, blank=True, choices=PERSON_GENDER_CHOICES)
    owner_birthday = models.DateField(_('birthday'), null=True, blank=True)
    owner_country = models.PositiveIntegerField(_('country'), null=True, blank=True)
    owner_index = models.CharField(_('postal index (ZIP)'), max_length=6, null=True, blank=True)
    owner_city = models.PositiveIntegerField(_('city'), null=True, blank=True)
    owner_city_custom = models.CharField(_('city (custom)'), max_length=50, null=True, blank=True)
    owner_address = models.CharField(_('address'), max_length=70, null=True, blank=True)
    owner_street = models.CharField(_('street'), max_length=50, null=True, blank=True)
    owner_house = models.CharField(_('house'), max_length=10, null=True, blank=True)
    owner_apartment = models.CharField(_('apartment'), max_length=10, null=True, blank=True)
    owner_phone = models.CharField(_('phone'), max_length=12, null=True, blank=True)
    owner_email = models.EmailField(_('email'), null=True, blank=True)

    # Доп. водитель 1
    ad1_pin = models.CharField(_('PIN'), max_length=9, null=True, blank=True)
    ad1_lname = models.CharField(_('last name'), max_length=50, null=True, blank=True)
    ad1_fname = models.CharField(_('first name'), max_length=50, null=True, blank=True)
    ad1_mname = models.CharField(_('middle name'), max_length=50, null=True, blank=True)
    ad1_gender = models.PositiveSmallIntegerField(_('gender'), null=True, blank=True, choices=PERSON_GENDER_CHOICES)
    ad1_birthday = models.DateField(_('birthday'), null=True, blank=True)
    ad1_country = models.PositiveIntegerField(_('country'), null=True, blank=True)
    ad1_index = models.CharField(_('postal index (ZIP)'), max_length=6, null=True, blank=True)
    ad1_city = models.PositiveIntegerField(_('city'), null=True, blank=True)
    ad1_city_custom = models.CharField(_('city (custom)'), max_length=50, null=True, blank=True)
    ad1_address = models.CharField(_('address'), max_length=70, null=True, blank=True)
    ad1_street = models.CharField(_('street'), max_length=50, null=True, blank=True)
    ad1_house = models.CharField(_('house'), max_length=10, null=True, blank=True)
    ad1_apartment = models.CharField(_('apartment'), max_length=10, null=True, blank=True)
    ad1_phone = models.CharField(_('phone'), max_length=12, null=True, blank=True)
    ad1_email = models.EmailField(_('email'), null=True, blank=True)

    # Доп. водитель 2
    ad2_pin = models.CharField(_('PIN'), max_length=9, null=True, blank=True)
    ad2_lname = models.CharField(_('last name'), max_length=50, null=True, blank=True)
    ad2_fname = models.CharField(_('first name'), max_length=50, null=True, blank=True)
    ad2_mname = models.CharField(_('middle name'), max_length=50, null=True, blank=True)
    ad2_gender = models.PositiveSmallIntegerField(_('gender'), null=True, blank=True, choices=PERSON_GENDER_CHOICES)
    ad2_birthday = models.DateField(_('birthday'), null=True, blank=True)
    ad2_country = models.PositiveIntegerField(_('country'), null=True, blank=True)
    ad2_index = models.CharField(_('postal index (ZIP)'), max_length=6, null=True, blank=True)
    ad2_city = models.PositiveIntegerField(_('city'), null=True, blank=True)
    ad2_city_custom = models.CharField(_('city (custom)'), max_length=50, null=True, blank=True)
    ad2_address = models.CharField(_('address'), max_length=70, null=True, blank=True)
    ad2_street = models.CharField(_('street'), max_length=50, null=True, blank=True)
    ad2_house = models.CharField(_('house'), max_length=10, null=True, blank=True)
    ad2_apartment = models.CharField(_('apartment'), max_length=10, null=True, blank=True)
    ad2_phone = models.CharField(_('phone'), max_length=12, null=True, blank=True)
    ad2_email = models.EmailField(_('email'), null=True, blank=True)

    # Доставка и оплата наследуется

    class Meta:
        app_label = 'calculator'
        verbose_name = 'vehicle contract'
        verbose_name_plural = 'vehicle contracts'


class PropertyContract(ContractCalculationAbstract):
    u"""
    Комплексный договор по страхованию недвижимости (ОСН)
    """

    # Общие данные о текущем расчете, условия договора
    p3_selected = models.BooleanField(_('product 3 selected'), default=False)
    p3_id = models.PositiveIntegerField(_('p3 document id'), null=True, blank=True)

    # Страхователь наследуется

    # Недвижимость
    realty_type = models.PositiveIntegerField(_('realty type'))
    city = models.PositiveIntegerField(_('city'))
    branch = models.PositiveIntegerField(_('branch'), null=True, blank=True)
    s_insurance = models.PositiveIntegerField(_('insurance sum'), null=True, blank=True)
    franchise = models.PositiveIntegerField(_('insurance sum'), null=True, blank=True)
    n_reestr = models.CharField(_('registry number'), max_length=50, null=True, blank=True)
    document_reason = models.CharField(_('document reason'), max_length=50, null=True, blank=True)
    using_method = models.PositiveIntegerField(_('using method'), null=True, blank=True)
    address = models.CharField(_('address'), max_length=100, null=True, blank=True)
    index = models.CharField(_('index'), max_length=6, null=True, blank=True)

    # Продукт ОСН
    p3_inscompany = models.PositiveSmallIntegerField(_('insurance company'), null=True, blank=True)

    # Доставка и оплата наследуется

    class Meta:
        app_label = 'calculator'
        verbose_name = 'property contract'
        verbose_name_plural = 'property contracts'


class TravelContract(ContractCalculationAbstract):
    u"""
    Комплексный договор по страхованию выезжающих за рубеж
    """
    # Общие данные о текущем расчете, условия договора
    p4_selected = models.BooleanField(_('product 4 selected'), default=False)
    p4_id = models.PositiveIntegerField(_('p4 document id'), null=True, blank=True)

    # Страхователь наследуется

    # Путешествие
    currency = models.PositiveIntegerField(_('currency'), null=True, blank=True)
    rest_type = models.PositiveIntegerField(_('rest type'), null=True, blank=True)
    countries = models.TextField(_('countries'), null=True, blank=True)
    ins_value = models.PositiveIntegerField(_('ins value'), null=True, blank=True)
    risk_group = models.PositiveIntegerField(_('risk group'), null=True, blank=True)
    # d_start унаследован
    d_end = models.DateField(_('contract date end'), null=True, blank=True)
    insured_days = models.PositiveIntegerField(null=True, blank=True)
    rest_term_year = models.BooleanField(_('one year contract'), default=False)

    # Застрахованный
    traveller_first_name = models.CharField(_('traveller first name'), max_length=100, null=True, blank=True)
    traveller_last_name = models.CharField(_('traveller last name'), max_length=100, null=True, blank=True)
    traveller_middle_name = models.CharField(_('traveller middle name'), max_length=100, null=True, blank=True)
    traveller_gender = models.PositiveSmallIntegerField(_('gender'), choices=PERSON_GENDER_CHOICES, default=1)
    traveller_n_passport = models.CharField(_('traveller n passport'), max_length=50, null=True, blank=True)
    traveller_birthday = models.DateField(_('traveller birthday'), null=True, blank=True)
    traveller_address = models.CharField(_('traveller address'), max_length=250, null=True, blank=True)
    traveller_pin = models.CharField(_('traveller pin'), max_length=10, null=True, blank=True)
    traveller_city = models.PositiveIntegerField(_('traveller city'), null=True, blank=True)

    # Специфика Ateshgah
    embassy = models.PositiveIntegerField(_('embassy'), null=True, blank=True)

    # Специфика AXA MBASK
    country_of_departure = models.PositiveIntegerField(null=True, blank=True)
    departure_type = models.PositiveIntegerField(null=True, blank=True)
    rest_type_extended = models.PositiveIntegerField(null=True, blank=True)

    # Продукт ВЗР
    p4_inscompany = models.PositiveSmallIntegerField(_('insurance company'), null=True, blank=True)

    # Доставка и оплата наследуется

    class Meta:
        app_label = 'calculator'
        verbose_name = 'travel contract'
        verbose_name_plural = 'travel contracts'


class HealthContract(ContractCalculationAbstract):
    """
    Комплексный договор по страхованию Здоровья. Продукты 9 ДО (Urgent Care, Refund Pediatric, Program 69)
    """
    p9_1_selected = models.BooleanField(_('product 9 urgent selected'), default=False)
    p9_2_selected = models.BooleanField(_('product 9 refund selected'), default=False)
    p9_3_selected = models.BooleanField(_('product 9 program 69 selected'), default=False)

    # Страхователь наследуется

    # Идентификаторы связанных документов - для каждого продукта свой
    p9_1_id = models.PositiveIntegerField(_('p9 urgent document id'), null=True, blank=True)
    p9_2_id = models.PositiveIntegerField(_('p9 refund document id'), null=True, blank=True)
    p9_3_id = models.PositiveIntegerField(_('p9 program 69 document id'), null=True, blank=True)

    # Оплаченные суммы
    p9_1_payment = models.DecimalField(_('Urgent Care payment'), max_digits=10, decimal_places=2, null=True, blank=True)
    p9_2_payment = models.DecimalField(_('REFUND payment'), max_digits=10, decimal_places=2, null=True, blank=True)
    p9_3_payment = models.DecimalField(_('Program 69 payment'), max_digits=10, decimal_places=2, null=True, blank=True)

    # Сроки страхованя по продуктам не сохраняются (1 год для refund и urgent, 5 лет для 69 и 69+)

    # Refund
    deductible = models.PositiveIntegerField(null=True, blank=True)
    refund_vip = models.BooleanField(_('refund vip'), default=False)
    vac = models.BooleanField(_('vaccination'), default=False)
    massage = models.BooleanField(_('massage'), default=False)
    program69_extended = models.BooleanField(_('program 69 extended'), default=False)
    health_poll = models.CharField(max_length=200, null=True, blank=True)

    # Информация о застрахованном
    insured_lname = models.CharField(_('insured last name'), max_length=50, null=True, blank=True)
    insured_fname = models.CharField(_('insured first name'), max_length=50, null=True, blank=True)
    insured_mname = models.CharField(_('insured middle name'), max_length=50, null=True, blank=True)
    insured_birthday = models.DateField(_('insured birthday'), null=True, blank=True)

    p9_inscompany = models.PositiveSmallIntegerField(_('insurance company'), null=True, blank=True)

    # Доставка и оплата наследуется

    class Meta:
        app_label = 'calculator'
        verbose_name = 'health_contract'
        verbose_name_plural = 'health_contracts'
