# coding=utf-8
from django.template.loader import render_to_string
from calculator.constants import PRODUCTS


def parse_get_tariff_response(tariffs):
    u"""
    Получаем тарифы по продуктам и раскладываем их в словарь
    tariffs_dict = {<company_id> : {<(str)product_id>: <value|None>, ...}, ...}
    :param tariffs: ответ от сервиса
    :return:
    """
    tariffs_dict = {}
    for t in tariffs.Tariff:
        if hasattr(t, 's_premium'):
            # Для того, чтобы не словить очень НЕЯВНУЮ ОШИБКУ product_id ВСЕГДА приводим к Юникоду
            product_id = unicode(t.sub_product if hasattr(t, 'sub_product') else t.product)
            if t.company in tariffs_dict:
                tariffs_dict[t.company].update({product_id: t.s_premium})
            else:
                tariffs_dict[t.company] = {product_id: t.s_premium}
    return tariffs_dict


def get_tariff_matrix_html(product_ids, ins_companies_qs, tariffs_dict):
    u"""
    Сборка структуры для отображения таблицы продуктов

    Строка заголовка:
    [ ['', '', <название продука 1>, <название продука 2>, ... ]

    Строки данных 1..n:
    [ [<company_id>, <company_title>, {'id': <product_id>, 'price': <product_price>}, {...}, ... ]
    :param product_ids:
    :param ins_companies_qs:
    :param tariffs_dict:
    :return:
    """
    template_params = {
        'products': [],
        'product_matrix': None
    }

    products_dict = {k: v['table_title'] for k, v in PRODUCTS.items() if k in product_ids}
    product_matrix = list()
    header_line = ['', '']
    for p in product_ids:
        header_line.append(products_dict[p])
    product_matrix.append(header_line)

    for c in ins_companies_qs:
        l = [c.id, c.title]
        for p in product_ids:
            # Ключ product_id приводится к Юникоду, из-за реализации функции parse_get_tariff_response, из которой
            # получаем значения в tariffs_dict
            company_id, product_id = c.id, unicode(p)
            if company_id in tariffs_dict and product_id in tariffs_dict[c.id]:
                l.append({'id': p, 'price': tariffs_dict[company_id][product_id]})
            else:
                l.append(None)
        product_matrix.append(l)

    template_params.update({
        'products': product_ids,
        'product_matrix': product_matrix
    })

    return render_to_string('calculator/product_matrix.html', template_params)