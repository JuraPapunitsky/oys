# coding=utf-8

import json
from django.http import HttpResponse

import logging
logger = logging.getLogger('core.ajax_response')


def ajax_response(function, *vargs, **kwargs):
    u""" Возврат результата в виде JSON
    с поддержкой перехвата исключений """

    def wraper(*vargs, **kwargs):
        try:
            result_dict = {"error": None, "result": function(*vargs, **kwargs)}

        except Exception as e:
            logger.error(unicode(e), exc_info=True)
            result_dict = {"error": unicode(e)}

        return HttpResponse(json.dumps(result_dict), content_type="application/json;charset=utf-8")

    return wraper
