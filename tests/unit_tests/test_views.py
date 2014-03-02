from __future__ import with_statement
import datetime
from contextlib import nested
from django.http import HttpResponseRedirect, HttpResponse
import mock
from Mindwell.Client import views
from Mindwell.Client import models
from django.test.utils import setup_test_environment
import mock_common
from google.appengine.ext import db
from google.appengine.api import users

setup_test_environment()


def mock_global_get_raises(*args):
    raise db.BadKeyError


class Test_change_user(mock_common.MockAppEngineTest):

    def test_change_user(self):
        with nested(
            mock.patch('Mindwell.Client.models.UserPermission.safe_get',
                       mock_common.static_mock_return_true)):
            req = mock_common.MockRequest()
            http_response = views.change_user(req, change_user='Fake User')
            self.assertIn('current_user', http_response.cookies)
            self.assertEqual('',
                             http_response.cookies['current_user']['expires'])

    def test_change_self(self):
        with nested(
            mock.patch('Mindwell.Client.models.UserPermission.safe_get',
                       mock_common.static_mock_return_true)):
            req = mock_common.MockRequest()
            http_response = views.change_user(req, change_user='Self')
            self.assertEqual('Thu, 01-Jan-1970 00:00:00 GMT',
                             http_response.cookies['current_user']['expires'])

    def test_bad_key_error(self):
        with nested(mock.patch('Mindwell.Client.models.global_get',
                               mock_global_get_raises)):
            req = mock_common.MockRequest()
            http_response = views.change_user(req, change_user='Fake User')
            self.assertIsInstance(http_response, HttpResponseRedirect)


class Test_redirect_to_base(mock_common.MockAppEngineTest):
    def test_redirect(self):
        self.assertIsInstance(views.redirect_to_base(None),
                              HttpResponseRedirect)


class Test_reports(mock_common.MockAppEngineTest):
    def test_redirect(self):
        req = mock_common.MockRequest()
        self.assertIsInstance(views.reports(req),
                              HttpResponse)


class Test_get_dos_balance(mock_common.MockAppEngineTest):
    def test_no_dos(self):
        self.assertEqual(0, views.get_dos_balance([]))

    def test_balance_due(self):
        dos = models.DOS(amt_due=str(1.0))
        self.assertEqual(1.0, views.get_dos_balance([dos]))

    def test_balance_paid(self):
        dos = models.DOS(amt_due=str(1.0), amt_paid=str(1.0))
        self.assertEqual(0, views.get_dos_balance([dos]))

    def test_overpaid(self):
        dos = models.DOS(amt_paid=str(1.0))
        self.assertEqual(-1.0, views.get_dos_balance([dos]))


class Test_generate_client_invoices(mock_common.MockAppEngineTest):

    def test_generate_no_dos(self):
        req = mock_common.MockRequest()
        http_response = views.generate_client_invoices(req, 2012, 1)
        self.assertEqual(http_response.status_code, 200)

    def test_generate_with_dos_repeat_call(self):
        self.test_generate_with_dos()
        # test that we don't bother generating a new invoice
        self.test_generate_with_dos()

    def test_generate_with_dos(self):
        req = mock_common.MockRequest()
        resp = views.generate_client_invoices(req, 2012, 1)
        self.assertEqual(resp.status_code, 200)
        self.assertRegexpMatches(
            resp.content,
            '.*/Mindwell/\d+/attended_only/invoice_display/.*')
        # check that we only generate one invoice
        self.assertEqual(len(models.Invoice.safe_all(req).fetch(3000)), 1)


class Test_generate_client_invoices_by_date(mock_common.MockAppEngineTest):

    def test_generate(self):
        req = mock_common.MockRequest()
        http_response = views.generate_client_invoices_by_date(
            req, 2012, 1, 1, 2012, 2, 1)

        self.assertEqual(http_response.status_code, 200)


class Test_invoices(mock_common.MockAppEngineTest):

    def test_no_invoices(self):
        views.invoices(mock_common.MockRequest())

    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'clientinfo': self.client.get_id(),
                                            'start_date_month': 1,
                                            'start_date_day': 1,
                                            'start_date_year': 2008,
                                            'end_date_month': 1,
                                            'end_date_day': 1,
                                            'end_date_year': 2022})
        resp = views.invoices(req)
        self.assertIsInstance(resp, HttpResponseRedirect)
        self.assertEqual(resp.status_code, 302)

        req = mock_common.MockRequest()
        resp = views.invoices(req)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)
        self.assertRegexpMatches(resp.content,
                                 '.*/Mindwell/\d+/all_dos/invoice_display/.*')


class Test_invoice_settings(mock_common.MockAppEngineTest):

    def test_no_invoice_setting(self):
        req = mock_common.MockRequest()
        http_response = views.invoice_settings(req)
        self.assertEqual(http_response.status_code, 200)

    def test_invoice_setting(self):
        req = mock_common.MockRequest()
        invoice_setting = models.InvoiceSettings(
            userinfo=users.get_current_user(),
            user_id = users.get_current_user().user_id(), practice_name='Test Practice')
        invoice_setting.put()
        http_response = views.invoice_settings(req)
        self.assertIn('Test Practice', http_response.content)


class Test_invoice_display(mock_common.MockAppEngineTest):
    def setUp(self):
        super(Test_invoice_display, self).setUp()
        self.client = models.ClientInfo(userinfo=users.get_current_user(),
                                        user_id = users.get_current_user().user_id())
        self.client.put()
        self.start = datetime.datetime(2012, 1, 1)
        self.end = datetime.date(2012, 2, 1)
        self.invoice = models.Invoice(clientinfo=self.client,
                                      userinfo=users.get_current_user(),
                                        user_id = users.get_current_user().user_id(),
                                      start_date=self.start.date(),
                                      end_date=self.end)
        self.invoice.put()

    def test_no_dos(self):
        req = mock_common.MockRequest()
        invoice_id = self.invoice.get_id()
        http_response = views.invoice_display(req, invoice_id)
        self.assertEqual(http_response.status_code, 200)
        http_response = views.invoice_display(req, invoice_id, html=True)
        self.assertEqual(http_response.status_code, 200)

    def test_with_dos(self):
        req = mock_common.MockRequest()
        dos = models.DOS(userinfo=users.get_current_user(),
                                        user_id = users.get_current_user().user_id(),
                         clientinfo=self.client,
                         dos_datetime=self.start)
        dos.put()
        invoice_id = self.invoice.get_id()
        http_response = views.invoice_display(req, invoice_id)
        self.assertEqual(http_response.status_code, 200)
        http_response = views.invoice_display(req, invoice_id, html=True)
        self.assertEqual(http_response.status_code, 200)


class Test_update_invoice_settings(mock_common.MockAppEngineTest):
    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'practice_name': 'Test Practice'})
        views.invoice_settings(req)
        req = mock_common.MockRequest()
        http_response = views.invoice_settings(req)
        self.assertIn('Test Practice', http_response.content)


class Test_calendar_settings(mock_common.MockAppEngineTest):

    def test_no_calendar_setting(self):
        req = mock_common.MockRequest()
        http_response = views.calendar_settings(req)

        self.assertEqual(http_response.status_code, 200)

    def test_calendar_setting(self):
        req = mock_common.MockRequest()
        calendar_setting = models.CalendarSettings(
            userinfo=users.get_current_user(),
                                        user_id = users.get_current_user().user_id(),
            calendar_start_time='5 am')
        calendar_setting.put()
        http_response = views.calendar_settings(req)
        self.assertIn('<option value="5 am" selected="selected">5 am</option>',
                      http_response.content)


class Test_update_calendar_settings(mock_common.MockAppEngineTest):

    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'calendar_start_time': '7 am',
                                            'display_weekends': 'No'})
        views.calendar_settings(req)
        req = mock_common.MockRequest()
        http_response = views.calendar_settings(req)
        self.assertIn('<option value="7 am" selected="selected">7 am</option>',
                      http_response.content)


class Test_custom_form_settings(mock_common.MockAppEngineTest):

    def test_no_custom_form_setting(self):
        req = mock_common.MockRequest()
        http_response = views.custom_form_settings(req)

        self.assertEqual(http_response.status_code, 200)

    def test_custom_form_setting(self):
        req = mock_common.MockRequest()
        custom_form_setting = models.CustomFormSettings(
            userinfo=users.get_current_user(),
                                        user_id = users.get_current_user().user_id(),
            reason_for_visit_choices='Reason1\nReason2')
        custom_form_setting.put()
        http_response = views.custom_form_settings(req)
        self.assertIn('Reason1\nReason2',
                      http_response.content)


class Test_update_custom_form_settings(mock_common.MockAppEngineTest):
    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={'reason_for_visit_choices':
                                            'Reason1\nReason2',
                                            'referrer_choices': '',
                                            'session_type_choices': '',
                                            'new_client_script': ''})
        views.custom_form_settings(req)
        req = mock_common.MockRequest()
        http_response = views.custom_form_settings(req)
        self.assertIn('Reason1\nReason2',
                      http_response.content)


class Test_run_export_provider_data(mock_common.MockAppEngineTest):
    def test_empty(self):
        req = mock_common.MockRequest()
        http_response = views.run_export_provider_data(req)
        self.assertEqual(http_response.status_code, 200)


class test_administrator(mock_common.MockAppEngineTest):
    def test_basic_get(self):
        req = mock_common.MockRequest()
        http_response = views.administrator(req)
        self.assertEqual(http_response.status_code, 200)


class Test_provider_invoices(mock_common.MockAppEngineTest):
    def test_basic_get(self):
        req = mock_common.MockRequest()
        resp = views.provider_invoices(req)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        req = mock_common.MockRequest(method='POST',
                                      POST={
            'start_invoice_date': datetime.datetime.now().date(),
            'end_invoice_date': datetime.datetime.now().date()})
        resp = views.provider_invoices(req)
        self.assertEqual(resp.status_code, 302)


class Test_provider_invoices_display(mock_common.MockAppEngineTest):
    def test_basic_get(self):
        req = mock_common.MockRequest()
        resp = views.provider_invoices_display(req, 2012, 1, 1, 2013, 1, 1)
        self.assertEqual(resp.status_code, 200)


class Test_provider_stats_all_time(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = views.provider_stats_all_time(req)
        self.assertEqual(resp.status_code, 200)


class Test_provider_statistics(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = views.provider_statistics(req)
        self.assertEqual(resp.status_code, 200)


class Test_provider_statistics_display(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = views.provider_statistics_display(req, 2013)
        self.assertEqual(resp.status_code, 200)


class Test_permission_settings(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = views.permission_settings(req)
        self.assertEqual(resp.status_code, 200)


class Test_update_permission_settings(mock_common.MockAppEngineTest):
    def test_get(self):
        req = mock_common.MockRequest()
        resp = views.update_permission_settings(req)
        self.assertEqual(resp.status_code, 302)
