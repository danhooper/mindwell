# -*- coding: utf-8 -*-
from __future__ import with_statement
import datetime
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.test.utils import setup_test_environment
from django.utils import simplejson
import mock_common
from google.appengine.api import users
from google.appengine.ext import db
from Mindwell.Client import client_views
from Mindwell.Client import models

setup_test_environment()


class Test_add_client_form(mock_common.MockAppEngineTest):

    def setUp(self):
        super(Test_add_client_form, self).setUp()
        self.get_req = mock_common.MockRequest()
        self.new_lastname = 'Test_add_client_form lastname'
        self.post_req = mock_common.MockRequest(
            method='POST', POST={'lastname': self.new_lastname})

    def test_get_form(self):
        http_response = client_views.add_client_form(self.get_req)
        self.assertEqual(http_response.status_code, 200)

    def test_post(self):
        clients = models.ClientInfo.safe_all(self.post_req)
        db.delete(clients)
        http_response = client_views.add_client_form(self.post_req)
        self.assertIsInstance(http_response, HttpResponseRedirect)
        self.assertEqual(clients[0].lastname, self.new_lastname)

    def test_post_secondary_user(self):
        self.post_req.COOKIES = {'current_user':
                                 str(self.user_permission.key())}
        http_response = client_views.add_client_form(self.post_req)
        self.assertIsInstance(http_response, HttpResponseRedirect)
        clients = models.ClientInfo.safe_all(self.post_req)
        self.assertEqual(clients[0].lastname, self.new_lastname)


class Test_add_client_standalone(mock_common.MockAppEngineTest):
    def test_get_form(self):
        req = mock_common.MockRequest()
        http_response = client_views.add_client_standalone(req)
        self.assertEqual(http_response.status_code, 200)

    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'lastname': 'fake lastname'})
        http_response = client_views.add_client_standalone(req)
        content_dict = simplejson.loads(http_response.content)
        self.assertIn('fake lastname', http_response.content)
        self.assertTrue(content_dict['key'])

    def test_post_unicode(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'lastname': 'é' * 10})
        http_response = client_views.add_client_standalone(req)
        content_dict = simplejson.loads(http_response.content)
        self.assertIn(u'é' * 10, content_dict['name'])
        self.assertTrue(content_dict['key'])


class Test_show_client(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        http_response = client_views.show_client(req)
        self.assertEqual(http_response.status_code, 200)


class Test_show_specific_client(mock_common.MockAppEngineTest):
    def test_post(self):
        start = datetime.datetime(2012, 1, 1)
        client = models.ClientInfo(userinfo=users.get_current_user())
        client.put()
        req = mock_common.MockRequest(method='POST',
                                      POST={'amt_due': 100,
                                            'dos_datetime_0':  start.date(),
                                            'dos_datetime_1_time': '12:00 am',
                                            'dos_endtime_time': '12:30 am'})
        http_response = client_views.show_specific_client(req, client.get_id())
        self.assertIsInstance(http_response, HttpResponseRedirect)
        req = mock_common.MockRequest()
        http_response = client_views.show_specific_client(req, client.get_id())
        self.assertIn('100', http_response.content)


class Test_show_client_letter(mock_common.MockAppEngineTest):
    def test_clients_exist(self):
        req = mock_common.MockRequest()
        http_response = client_views.show_client_letter(req, 'F')
        self.assertIn('fake lastname', http_response.content)
        http_response = client_views.show_client_letter(req, 'A')
        self.assertNotIn('fake lastname', http_response.content)

    def test_no_clients_exist(self):
        req = mock_common.MockRequest()
        http_response = client_views.show_client_letter(req, 'G')
        self.assertNotIn('fake lastname', http_response.content)


class Test_dos_receipt(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        http_response = client_views.dos_receipt(req, self.dos.get_id())
        self.assertIsInstance(http_response, HttpResponse)

    def test_invalid_dos(self):
        req = mock_common.MockRequest()
        http_response = client_views.dos_receipt(req, 1000)
        self.assertIsInstance(http_response, HttpResponseRedirect)


class Test_search(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = client_views.search(req)
        self.assertEqual(resp.status_code, 200)


class Test_search_result(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = client_views.search_result(req, 'a')
        self.assertEqual(resp.status_code, 200)


class Test_update_client(mock_common.MockAppEngineTest):
    def test_get(self):
        client = models.ClientInfo(userinfo=users.get_current_user())
        client.put()
        req = mock_common.MockRequest()
        resp = client_views.update_client(req, client.get_id())
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'lastname': 'test_lastname123'})
        resp = client_views.update_client(req, self.client1.get_id())
        self.assertIsInstance(resp, HttpResponseRedirect)
        client = models.ClientInfo.safe_all()[0]
        self.assertEqual(client.lastname, 'test_lastname123')


class Test_update_dos(mock_common.MockAppEngineTest):
    def test_get(self):
        client = models.ClientInfo(userinfo=users.get_current_user(),
                                   lastname='fake lastname',
                                   firstname='fake firstname')
        client.put()
        start = datetime.datetime(2012, 1, 1)
        dos = models.DOS(userinfo=users.get_current_user(),
                         clientinfo=client,
                         dos_datetime=start)
        dos.put()
        req = mock_common.MockRequest()
        resp = client_views.update_dos(req, dos.get_id())
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp, HttpResponse)

    def test_post(self):
        start = datetime.datetime(2012, 1, 1)
        req = mock_common.MockRequest(method='POST',
                                      POST={'amt_due': 100,
                                            'dos_datetime_0':  start.date(),
                                            'dos_datetime_1_time': '12:00 am',
                                            'dos_endtime_time': '12:30 am'})
        resp = client_views.update_dos(req, self.dos.get_id())
        self.assertEqual(resp.status_code, 302)
        self.assertIsInstance(resp, HttpResponseRedirect)
        dos = models.DOS.safe_all()[0]
        self.assertEqual(int(dos.amt_due), 100)


class Test_delete_client(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = client_views.delete_client(req, self.client1.get_id())
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp, HttpResponse)

    def test_post(self):
        req = mock_common.MockRequest(method='POST')
        resp = client_views.delete_client(req, self.client1.get_id())
        resp = client_views.delete_client(req, self.client2.get_id())
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp, HttpResponse)
        json_data = json.loads(resp.content)
        self.assertEqual(json_data.get('message'), 'Success')

        client = models.ClientInfo.safe_all().fetch(100)
        self.assertFalse(client)
        dos = models.DOS.safe_all().fetch(100)
        self.assertFalse(dos)



