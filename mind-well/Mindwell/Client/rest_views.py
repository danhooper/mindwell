import json
import logging

from django.http import HttpResponse
from google.appengine.ext import db

import common
import context_processors
import models
import view_common


def rest_dos(request):
    if request.method == 'GET':
        dos = models.DOS.safe_all(request=request).fetch(
            common.get_maximum_num_dos_fetch())
        resp = HttpResponse(json.dumps([d.get_rest() for d in dos]),
                            content_type="application/json")
        return resp
    elif request.method == 'POST':
        pass


def rest_clientinfo(request):
    if request.method == 'GET':
        clients = models.ClientInfo.safe_all(request=request).fetch(
            common.get_maximum_num_dos_fetch())
        resp = HttpResponse(json.dumps([c.get_rest() for c in clients]),
                            content_type="application/json")
        return resp
    elif request.method == 'POST':
        post_dict = json.loads(request.raw_post_data)
        form = models.ClientForm(post_dict)
        if form.is_valid():
            entity = models.ClientInfo(**form.cleaned_data)
            view_common.save_entity(request, entity)
            return HttpResponse(json.dumps(entity.get_rest()),
                                content_type='application/json')
        else:
            errors = [(k, unicode(v[0]))
                      for k, v in form.errors.items()]
            return HttpResponse(json.dumps({'success': False,
                                            'errors': errors}),
                                content_type='application/json')


def rest_indiv_client(request, client_id):
    client_id = int(client_id)
    client = models.ClientInfo.safe_get_by_id(client_id, request)
    if not client:
        view_common.log_access_violation('delete_client')
        # TODO Error response
        return ''
    if request.method == 'GET':
        resp = HttpResponse(json.dumps(client.get_rest()),
                            content_type='application/json')
        return resp
    elif request.method == 'PUT':
        put_dict = json.loads(request.raw_post_data)
        form = models.ClientForm(put_dict)
        if form.is_valid():
            client.update_model(form.cleaned_data)
            view_common.save_entity(request, client)
            return HttpResponse(json.dumps(client.get_rest()),
                                content_type='application/json')
    elif request.method == 'DELETE':
        common.delete_client(client)
        resp = HttpResponse('', content_type='application/json')
        return resp
    elif request.method == 'OPTIONS':
        resp = HttpResponse('')
        resp['Content-Length'] = '0'
        return resp


def rest_custom_form_settings(request):
    if request.method == 'GET':
        cf_settings = models.CustomFormSettings.GetSettings(request=request)
        return HttpResponse(json.dumps([cf_settings.get_rest()]),
                            content_type='application/json')


def rest_user_perm(request):
    if request.method == 'GET':
        perm_users = context_processors.get_permitted_users(request)
        perm_users = perm_users['permitted_users']
        return HttpResponse(
            json.dumps([user.get_rest() for user in perm_users]),
            content_type='application/json')

