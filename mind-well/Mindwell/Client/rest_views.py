import json
import logging

from django.http import HttpResponse
from google.appengine.ext import db

import common
import models

def add_response_headers(response, request):
    if request.META['SERVER_NAME'] == 'havok':
        response['Access-Control-Allow-Origin'] = 'http://havok:9001'
        response['Access-Control-Allow-Credentials'] = 'true'

def rest_dos(request):
    if request.method == 'GET':
        dos = models.DOS.safe_all(request=request).fetch(
            common.get_maximum_num_dos_fetch())
        resp = HttpResponse(json.dumps([d.get_rest() for d in dos]), content_type="application/json")
        add_response_headers(resp, request)
        return resp
    elif request.method == 'POST':
        pass

def rest_clientinfo(request):
    if request.method == 'GET':
        clients = models.ClientInfo.safe_all(request=request).fetch(
            common.get_maximum_num_dos_fetch())
        resp = HttpResponse(json.dumps([c.get_rest() for c in clients]), content_type="application/json")
        add_response_headers(resp, request)
        return resp
    elif request.method == 'POST':
        pass
