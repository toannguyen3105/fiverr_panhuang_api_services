#!/usr/bin/env python
# -*- coding: utf-8 -*-

STATUS_CODES = ['OK', 'INTERNAL_ERROR', 'DATABASE_ERROR', "ACCOUNT_EXISTED", "NOT_FOUND"]

from utils.date_format import getTimeStamp


def generate_response(error, status, result, http_code):
    return {
               "error": error,
               "status": STATUS_CODES[status],
               "result": result,
               "timestamp": getTimeStamp()
           }, http_code
