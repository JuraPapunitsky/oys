# coding=utf-8
from django.utils.translation import ugettext_lazy as _

# Компании (значение), продающие договора по продуктам (ключ)
PRODUCT_COMPANIES = {
    2: (1, 3, 5, 6, 8, 11, 12),
    3: (1, 3, 5, 6, 8, 12),
    4: (1, 5, 8, 11, 12),
    9: (10, ),
    11: (10, ),
    12: (8, ),
}

# Продукты
PRODUCTS = {
    2: {
        'title': _(u'ОСАГО'),
        'table_title': _(u'ОСАГО'),
        'description': _(u'Обязательное страхование ответственности автовладельцев перед 3-ми лицами')
    },
    3: {
        'title': _(u'ОС Недвижимости'),
        'table_title': _(u'ОС Недвижимости'),
        'description': _(u'Страхование от ущерба, причиненный конструктивным элементам, помещениям, в том числе '
                         u'дверным и оконным конструкциям, включая стекла, трубам систем водоснабжения, канализации и '
                         u'газоснабжения, а также тепловой системы, проводам связи, электрическим и иным проводам, '
                         u'элементам украшения, в том числе всем видам внешних или внутренних штукатурных работ, '
                         u'стенам, потолку и полу')
    },
    4: {
        'title': _(u'Страхование путешественников'),
        'table_title': _(u'Страхование путешественников'),
        'description': _(u'Защита от непредвиденных расходов, связанных с предоставлением застрахованному медицинской, '
                         u'юридической, административной и иной помощи за границей')
    },
    '9_1': {
        'title': 'Urgent Care',
        'table_title': 'Urgent Care',
        'description': _(u'Лечение и обеспечение медикаментами во время неотложной помощи (вкл. стоматологию и '
                         u'вакцинацию)')
    },
    '9_2': {
        'title': 'REFUND Pediatric',
        'table_title': 'REFUND Pediatric',
        'description': _(u'Добровольное медицинское страхование (патронаж новорожденных, возмещение расходов на скорую '
                         u'помощь, амбулаторную помощь, стационарную помощь, стоматологию, физиотерапию и т.д.)')
    },
    '9_3': {
        'title': _(u'Программа 69'),
        'table_title': _(u'Программа 69'),
        'description': _(u'Лечение при диагностировании злокачественного онкозаболевания')
    },
    11: {
        'title': _(u'КАСКО: Уверенный водитель'),
        'table_title': _(u'Уверенный водитель'),
        'description': _(u'Полноценное страхование вашего автомобиля от ущерба, гибели, угон и противоправных действий '
                         u'3х лиц. Страховая выплата только в случае вашей невиновности.')
    },
    12: {
        'title': _(u'КАСКО: Простое КАСКО'),
        'table_title': _(u'Простое КАСКО'),
        'description': _(u'Самое доступное каско с возможностью застраховать Ваш автомобиль от ущерба на сумму до '
                         u'5000 AZN')
    }
}

# Костыль №1 (из-за того,что справочники тянутся через сервис)
# Меппинговый словарь дефолтных значений расширенного типа отдыха (LibTable4_80) для типов отдыха ASAN (LibTable4_10)
DEFAULT_AXA_EXTENDED_REST = {
    1: 13,
    2: 18,
    3: 3,
    4: 13,
    5: 15,
    6: 13,
    7: 18
}

# Костыль №2 (из-за того,что справочники тянутся через сервис)
# Списки доступных расширеных типов отдыха (LibTable4_80) для типов отдыха ASAN (LibTable4_10)
AXA_EXTENDED_REST_MAP = {
    1: (4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
    2: (18, ),
    3: (1, 2, 3),
    4: (4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
    5: (14, 15),
    6: (4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
    7: (18, )
}

DEFAULT_COUNTRY_OF_DEPARTURE = 4

HEALTH_POLL_OPTIONS = (
    {'id': 1, 'title': _(u'Травмы, повреждения/дефекты, их последствия. Имеются ли привычные вывихи/ '
                         u'ограничения движений суставов')},
    {'id': 2, 'title': _(u'Доброкачественные опухоли')},
    {'id': 3, 'title': _(u'Проблемы со спиной или  с позвоночником. Имеются ли видимые пороки развития '
                         u'опорно-двигательного аппарат (плоскостопие, косолапость, синдактилии, кривошея, '
                         u'воронкообразная грудь')},
    {'id': 4, 'title': _(u'Принимает ли Ваш ребенок сейчас какое-либо лечение или лекарство?')},
    {'id': 5, 'title': _(u'Частые заболевания пищевода/желудка/ кишечника')},
    {'id': 6, 'title': _(u'Частые легочные заболевания')},
    {'id': 7, 'title': _(u'Заболевания почек/ мочевого тракта')},
    {'id': 8, 'title': _(u'Есть ли у Вашего ребенка врожденные и наследственные заболевания')},
    {'id': 9, 'title': _(u'Болезни печени/ поджелудочной железы')},
    {'id': 10, 'title': _(u'Ревматизм/заболевания мышц, суставов, костей')},
    {'id': 11, 'title': _(u'Детский церебральный паралич (ДЦП), эпилепсия')},
    {'id': 12, 'title': _(u'Операции на головном мозге')},
    {'id': 13, 'title': _(u'Заболевания сосудов')},
    {'id': 14, 'title': _(u'Эндокринные заболевания')},
    {'id': 15, 'title': _(u'Аллергия')},
    {'id': 16, 'title': _(u'Повышение артериального  давления')},
    {'id': 17, 'title': _(u'Неврологические заболевания, миопатии')},
    {'id': 18, 'title': _(u'Нарушения ритма, проводимости сердца')},
    {'id': 19, 'title': _(u'Заболевания крови лейкемия/ лимфогранулематоз/ гемофилия /талассемия')},
    {'id': 20, 'title': _(u'Пороки сердца')},
    {'id': 21, 'title': _(u'Бронхиальная астма')},
    {'id': 22, 'title': _(u'Сахарный диабет')},
    {'id': 23, 'title': _(u'Является ли Ваш ребенок ВИЧ-инфицированным?')},
    {'id': 24, 'title': _(u'Злокачественные опухоли')},
    {'id': 25, 'title': _(u'Имеет ли Ваш ребенок инвалидность?')},
)

# Интервалы доставки
DELIVERY_INTERVALS = (
    (1, '09:00 - 10:00'),
    (2, '10:00 - 11:00'),
    (3, '11:00 - 12:00'),
    (4, '12:00 - 13:00'),
    (5, '13:00 - 14:00'),
    (6, '14:00 - 15:00'),
    (7, '15:00 - 16:00'),
    (8, '16:00 - 17:00'),
    (9, '17:00 - 18:00'),
    (10, '18:00 - 19:00'),
    (11, '19:00 - 20:00'),
)

# Регион доставки
DELIVERY_REGION = (
    (u'Binəqədi', u'Binəqədi'),
    (u'Yasamal', u'Yasamal'),
    (u'Xətai', u'Xətai'),
    (u'Xəzər', u'Xəzər'),
    (u'Nərimanov', u'Nərimanov'),
    (u'Nəsimi', u'Nəsimi'),
    (u'Nizami', u'Nizami'),
    (u'Səbail', u'Səbail'),
    (u'Sabunçu', u'Sabunçu'),
    (u'Suraxanı', u'Suraxanı'),
    (u'Qaradağ', u'Qaradağ'),
    (u'Pirallahı', u'Pirallahı'),
    (u'Digər', u'Digər'),
)

# Преобразование имен полей для страхователя (ОСАГО)
OSAGO_INSURANT_FIELDS_MAP = {
    'fld_first_name': 'ins_person_fname',
    'fld_last_name': 'ins_person_lname',
    'fld_middle_name': 'ins_person_mname',
    'fld_gender': 'ins_person_gender',
    'fld_birthday': 'ins_person_birthday',
    'fld_country': 'ins_country',
    'fld_city': 'ins_city',
    'fld_city_custom': 'ins_city_custom',
    'fld_address': 'ins_address',
    'fld_index': 'ins_index',
    'fld_street': 'ins_street',
    'fld_house': 'ins_house',
    'fld_apartment': 'ins_apartment',
    'fld_phone': 'ins_phone',
    'fld_email': 'ins_email',
}

# Поля страхователя (ОСН, ВЗР)
INSURANT_FIELDS_MAP = {
    'fld_pin': 'ins_person_pin',
    'fld_first_name': 'ins_person_fname',
    'fld_last_name': 'ins_person_lname',
    'fld_middle_name': 'ins_person_mname',
    'fld_gender': 'ins_person_gender',
    'fld_birthday': 'ins_person_birthday',
    'fld_country': 'ins_country',
    'fld_city': 'ins_city',
    'fld_city_custom': 'ins_city_custom',
    'fld_address': 'ins_address',
    'fld_index': 'ins_index',
    'fld_street': 'ins_street',
    'fld_house': 'ins_house',
    'fld_apartment': 'ins_apartment',
    'fld_phone': 'ins_phone',
    'fld_email': 'ins_email',
}

# Преобразование имен полей для владельца ТС (Простое КАСКО)
OWNER_FIELDS_MAP = {
    'fld_first_name': 'owner_fname',
    'fld_last_name': 'owner_lname',
    'fld_middle_name': 'owner_mname',
    'fld_gender': 'owner_gender',
    'fld_birthday': 'owner_birthday',
    'fld_pin': 'owner_pin',
    'fld_country': 'owner_country',
    'fld_city': 'owner_city',
    'fld_city_custom': 'owner_city_custom',
    'fld_address': 'owner_address',
    'fld_index': 'owner_index',
    'fld_street': 'owner_street',
    'fld_house': 'owner_house',
    'fld_apartment': 'owner_apartment',
    'fld_phone': 'owner_phone',
    'fld_email': 'owner_email',
}

# Преобразование имен полей для доп водителя 1 (Простое КАСКО)
AD1_FIELDS_MAP = {
    'fld_first_name': 'ad1_fname',
    'fld_last_name': 'ad1_lname',
    'fld_middle_name': 'ad1_mname',
    'fld_gender': 'ad1_gender',
    'fld_birthday': 'ad1_birthday',
    'fld_pin': 'ad1_pin',
    'fld_country': 'ad1_country',
    'fld_city': 'ad1_city',
    'fld_city_custom': 'ad1_city_custom',
    'fld_address': 'ad1_address',
    'fld_index': 'ad1_index',
    'fld_street': 'ad1_street',
    'fld_house': 'ad1_house',
    'fld_apartment': 'ad1_apartment',
    'fld_phone': 'ad1_phone',
    'fld_email': 'ad1_email',
}

# Преобразование имен полей для доп водителя 2 (Простое КАСКО)
AD2_FIELDS_MAP = {
    'fld_first_name': 'ad2_fname',
    'fld_last_name': 'ad2_lname',
    'fld_middle_name': 'ad2_mname',
    'fld_gender': 'ad2_gender',
    'fld_birthday': 'ad2_birthday',
    'fld_pin': 'ad2_pin',
    'fld_country': 'ad2_country',
    'fld_city': 'ad2_city',
    'fld_city_custom': 'ad2_city_custom',
    'fld_address': 'ad2_address',
    'fld_index': 'ad2_index',
    'fld_street': 'ad2_street',
    'fld_house': 'ad2_house',
    'fld_apartment': 'ad2_apartment',
    'fld_phone': 'ad2_phone',
    'fld_email': 'ad2_email',
}
