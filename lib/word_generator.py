# coding=utf-8

import os
from StringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
from lib.utils import render_string


class WordGenerator(object):
    def __init__(self, path):
        self._path = path
        self._zip_stream = StringIO()

    def _get_zip(self, context):
        zip_file = ZipFile(self._zip_stream, mode='a', compression=ZIP_DEFLATED)
        for path, dirs, files in os.walk(self._path):
            rel_path = path[len(self._path):]
            
            for file_name in files:
                if rel_path == '':
                    zip_name = file_name
                else:
                    zip_name = os.path.join(rel_path, file_name)

                absolute_path = os.path.join(path, file_name)
                
                if file_name == 'document.xml':
                    with open(absolute_path, 'r') as fh:
                        content = fh.read().decode('utf-8')  # в utf
                        content = render_string(content, context)
                        zip_file.writestr('word/document.xml', content.encode('utf-8'))  # в str
                else:
                    zip_file.write(absolute_path, zip_name)

        return zip_file

    def get_content(self, context):
        zip_file = self._get_zip(context)
        zip_file.close()
        return self._zip_stream.getvalue()