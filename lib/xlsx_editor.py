# coding=utf-8

u"""
Редактор xlsx

Пример использования:
from lib.xlsx_editor import XLSXEdit

xlsx = XLSXEdit('path_to_unzip_folder')

xlsx.write('Sheet1', 'A1', 333)
xlsx.write('Sheet1', 'A2', 44444)
xlsx.write('Sheet1', 'A3', datetime.now())
xlsx.write('Sheet1', 'A4', u'Строка')

with open('/Users/dibrovsd/Desktop/out.xlsx', 'w') as zip_file:
    zip_file.write(xlsx.get_content())

"""

import os
import re
from datetime import datetime, date
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree


class XLSXEdit(object):
    u""" 
    Редактирование файла xlsx через прямую модификацию файлов xml
    
    Зачем:
    Это бываем нужным, когда есть большой с кучей формул и картинок, макросов, объектов медиа-арт, 
    разных внедренных объектов, MS query настроек (кто-то знал excel)
    и нужно просто в пару ячеек вставить значения 
    
    Особенности:
    Мы аккуратно правим отдельные куски XML внутри и не трогаем все остальное
    """

    def __init__(self, zip_folder):
        u"""
        @param zip_folder: Путь к директории, где лежит распакованный исходный файл xlsx
        То есть файл '[Content_Types].xml' должен находится в этой директории
        """
        self._zip_folder = zip_folder
        self._data = {}
        self._zip_stream = StringIO()
        self._row_finder = re.compile(r'\d+$')
        self._namespaces = {
            'ws': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
            'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'
        }

        self._sheet_paths = self._get_sheet_locations()
        
        # Словарь строк
        self._shared_strings = None
        self._shared_strings_root = None
        self._shared_strings_index = None

    def write(self, sheet, cell, value):
        u""" 
        Установить значение для ячейки на листе
        Набирает все изменения в память.
        Они применяться только в момент сборки файл-архива xlsx
        
        @param sheet: Название листа
        @param cell: Название ячейки (например C4)
        @param value: Значение для записи в ячейку
        """

        if value is not None and type(value) not in (int, float, str, unicode, date, datetime):
            raise TypeError(u'Только None, int, float, str, unicode')

        if sheet not in self._data:
            self._data[sheet] = {}
        self._data[sheet][cell] = value

    def get_content(self):
        u""" 
        Получить контент файл xlsx с изменениями. 
        Листы, которые будут вставлены с изменениями, не включаем 
        """

        exclude_files = ['/%s' % e[1] for e in self._sheet_paths.items() if e[0] in self._data.keys()]
        exclude_files.append('/xl/sharedStrings.xml')

        zip_file = self._create_base_zip(exclude_files=exclude_files)
        self._add_changes(zip_file)

        zip_file.writestr('xl/sharedStrings.xml', 
                          etree.tostring(self._shared_strings, 
                                         xml_declaration=True, 
                                         encoding="UTF-8", 
                                         standalone="yes"))

        zip_file.close()
        
        return self._zip_stream.getvalue()

    def _get_xml(self, file_path):
        u""" 
        Вытащить XML-объект из папки по пути 
        @param file_path: Путь к файлу относительно директории шаблона
        """
        return etree.parse(os.path.join(self._zip_folder, file_path))

    def _init_shared_strings(self):
        u""" 
        Ленивым образом инициализируем работу со словарем строк.
        Лениво - потому что работа со строками может не понадобиться.
        Вызывается при первом вызове self._add_shared_string
        """
        self._shared_strings = self._get_xml('xl/sharedStrings.xml')
        self._shared_strings_root = self._shared_strings.xpath('/ws:sst', namespaces=self._namespaces)[0]
        self._shared_strings_index = int(self._shared_strings_root.attrib['uniqueCount'])

    def _add_shared_string(self, value):
        u""" 
        Добавить строку в словарь sharedStrings
        Не учитывает тот момент, что строка уже может тут быть.
        Но из-за малого кол-ва модификаций пофигу на раздувание словаря.
        uniqueCount и Count не модифицирует (и без этого все работает)

        @param value: Строка для добавления в словарь
        @return: Индекс в словаре sharedStrings
        """
        if self._shared_strings is None:
            self._init_shared_strings()

        node_t = etree.Element('t')
        node_t.text = value

        node_si = etree.Element('si')
        node_si.append(node_t)

        self._shared_strings_root.append(node_si)
        self._shared_strings_index += 1

        return (self._shared_strings_index - 1)

    def _get_sheet_locations(self):
        u""" 
        Узнаем где хранятся листы
        @return: Словарь. {название_листа: путь_к_xml}
        """
        
        # Книги
        sheets_id = {}
        workbook_xml = self._get_xml('xl/workbook.xml')
        for sheet_xml in workbook_xml.xpath('/ws:workbook/ws:sheets/ws:sheet', namespaces=self._namespaces):
            sheet_name = sheet_xml.attrib['name']
            sheet_rid = sheet_xml.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            sheets_id[sheet_rid] = sheet_name

        # Названия файлов
        paths = {}
        xml = self._get_xml('xl/_rels/workbook.xml.rels')
        for node in xml.xpath('/rel:Relationships/rel:Relationship', namespaces=self._namespaces):
            r_id = node.attrib['Id']
            path = os.path.join('xl', node.attrib['Target'])

            if r_id in sheets_id:
                sheet_label = sheets_id[r_id]
                paths[sheet_label] = path

        return paths    

    def _create_base_zip(self, exclude_files):
        u""" 
        Создать базовый объект на основе шаблона в папке zip_folder для модификации.
        В него не входят листы с изменными ячейками.
        Они будут добавлены туда в методе _add_changes
        @param exclude_files: Список исключенных файлов
        @return: объект ZipFile
        """

        zip_file = ZipFile(self._zip_stream, mode='a', compression=ZIP_DEFLATED)

        for path, dirs, files in os.walk(self._zip_folder):
            rel_path = path[len(self._zip_folder):]
            
            for file_name in files:
                if rel_path == '':
                    zip_name = file_name
                else:
                    zip_name = os.path.join(rel_path, file_name)

                if zip_name not in exclude_files:
                    zip_file.write(os.path.join(path, file_name), zip_name)

        return zip_file

    def _add_changes(self, zip_file):
        u""" 
        Применить изменения.
        Открываем и модифицируем файлы и заливаем их в zip поверх файлов по умолчанию

        @param zip_file: объект ZipFile без листов, на которых есть измененные ячейки
        """
        
        # Обходим листы и модифицируем
        for sheet_name, data in self._data.items():
            sheet_file = self._sheet_paths[sheet_name]
            
            sheet_content = self._get_changed_sheet(sheet_file=sheet_file, data=data)
            zip_file.writestr(sheet_file, sheet_content)

    def _get_changed_sheet(self, sheet_file, data):
        u""" 
        Возвращает отредактированный файл с данными для записи в ZIP-архив 
        @param sheet_file: Путь к xml-файлу с листом
        @param data: Словарь с изменениями {cell: value}
        @return: xml-строка с измененным листом
        """

        xml = etree.parse(os.path.join(self._zip_folder, sheet_file))
        for cell, value in data.items():
            self._change_cell(xml, cell, value)

        return etree.tostring(xml, xml_declaration=True, encoding="UTF-8", standalone="yes")

    def _change_cell(self, xml, cell, value):
        u""" 
        Изменить параметр ячейки в листе xml 
        Мутабельный метод по отношению к параметру xml
        
        @param xml: Объект lxml
        @param cell: Индекс ячейки в формате "C2"
        @param value: Значение
        """

        row_index = self._row_finder.search(cell).group()
        value_type = type(value)

        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_c = xml.xpath(pattern, namespaces=self._namespaces)[0]
        node_v = node_c.find('ws:v', namespaces=self._namespaces)
        
        # В шаблоне было пусто - добавим туда значение
        if node_v is None:
            node_v = etree.Element('v')
            node_c.append(node_v)

        # Пусто
        if value == None:
            node_c.remove(node_v)
            if node_c.attrib.get('t') == 's':
               del node_c.attrib['t']

        # Расшареная строка
        elif value_type in (unicode, str):
            value = str(self._add_shared_string(value))
            node_c.attrib['t'] = 's'

        # Числовые или приравненные к ним данные
        else:
            if node_c.attrib.get('t') == 's':
               del node_c.attrib['t']

            if value_type == datetime:
                value = value.date()

            if value_type == date:
                value = (value - date(1899, 12, 30)).days

        node_v.text = unicode(value)



