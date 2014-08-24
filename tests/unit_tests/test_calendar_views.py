import datetime
import json
import time
import unittest
from django.http import HttpResponseRedirect, HttpResponse
from django.test.utils import setup_test_environment
from google.appengine.api import users
import mock_common
from Mindwell.Client import calendar_views
from Mindwell.Client import models

setup_test_environment()


class TestCalendarLinks(unittest.TestCase):
    def test_get_urls(self):
            dos_date = datetime.datetime(2012, 5, 1)
            link = calendar_views.CalendarLinks(weekdate=dos_date)
            self.assertEqual('/Mindwell/2012/05/01/1/calendar_print_receipt/',
                             link.get_receipt_absolute_url(1))
            self.assertEqual('/Mindwell/2012/05/01/calendar/',
                             link.get_absolute_url())


class Test_calendar_display(mock_common.MockAppEngineTest):
    def test_get_no_date(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_display(req)
        self.assertIsInstance(resp, HttpResponseRedirect)

    def test_get(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_display(
            req, year=self.dos_start_datetime.year,
            month=self.dos_start_datetime.month,
            day=self.dos_start_datetime.day,
            hour=self.dos_start_datetime.hour,
            minute=self.dos_start_datetime.minute,
            dos_id=self.dos.get_id())
        self.assertIsInstance(resp, HttpResponse)

    def test_get_dos_recurr(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_display(
            req, year=self.dos_start_datetime.year,
            month=self.dos_start_datetime.month,
            day=self.dos_start_datetime.day,
            hour=self.dos_start_datetime.hour,
            minute=self.dos_start_datetime.minute,
            dos_recurr_id=self.dos.get_id())
        self.assertIsInstance(resp, HttpResponse)

    def test_invalid_dos(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_display(
            req, year=self.dos_start_datetime.year,
            month=self.dos_start_datetime.month,
            day=self.dos_start_datetime.day,
            hour=self.dos_start_datetime.hour,
            minute=self.dos_start_datetime.minute,
            dos_id=100)
        self.assertIsInstance(resp, HttpResponseRedirect)

    def test_invaid_dos_recurr(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_display(
            req, year=self.dos_start_datetime.year,
            month=self.dos_start_datetime.month,
            day=self.dos_start_datetime.day,
            hour=self.dos_start_datetime.hour,
            minute=self.dos_start_datetime.minute,
            dos_recurr_id=100)
        self.assertIsInstance(resp, HttpResponseRedirect)

    def test_post(self):
        start = datetime.datetime(2012, 1, 1)
        req = mock_common.MockRequest(method='POST',
                                      POST={'amt_due': 100,
                                            'dos_datetime_0':  start.date(),
                                            'dos_datetime_1_time': '12:00 am',
                                            'dos_endtime_time': '12:30 am'})

        calendar_views.calendar_display(req, 2012, 10, 1)
        dos = models.DOS.safe_all(req)[1]
        self.assertEqual(int(dos.amt_due), 100)


class Test_calendar_feed(mock_common.MockAppEngineTest):

    def setUp(self):
        super(Test_calendar_feed, self).setUp()
        now = datetime.datetime.now()
        start_datetime = (now - datetime.timedelta(days=30))
        start = start_datetime.strftime('%Y-%m-%d')
        end_datetime = (now + datetime.timedelta(days=30))
        end = end_datetime.strftime('%Y-%m-%d')
        self.req = mock_common.MockRequest(GET={
            'start': start,
            'end': end})

    def test_get_no_start(self):
        req = mock_common.MockRequest()
        resp = calendar_views.calendar_feed(req)
        self.assertIsInstance(resp, HttpResponse)

    def test_get_no_end(self):
        req = mock_common.MockRequest(GET={'start': 'fake'})
        resp = calendar_views.calendar_feed(req)
        self.assertIsInstance(resp, HttpResponse)

    def test_with_no_dos(self):
        resp = calendar_views.calendar_feed(self.req)
        self.assertIsInstance(resp, HttpResponse)

    def test_with_dos(self):
        self.dos_datetime = datetime.datetime.now()
        self.dos = models.DOS(dos_datetime=self.dos_datetime,
                              userinfo=users.get_current_user())
        self.dos.put()
        resp = calendar_views.calendar_feed(self.req)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Scheduled', resp.content)
        result = json.loads(resp.content)
        self.assertEqual(len(result), 1)

    def test_with_dos_recurr(self):
        self.dos_datetime = datetime.datetime.now()
        self.dos = models.DOS(dos_datetime=self.dos_datetime,
                              userinfo=users.get_current_user(),
                              dos_repeat='One Day')
        self.dos.put()
        resp = calendar_views.calendar_feed(self.req)
        self.assertIsInstance(resp, HttpResponse)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Scheduled', resp.content)
        result = json.loads(resp.content)
        self.assertGreater(len(result), 1)


class Test_calendar_update_dos(mock_common.MockAppEngineTest):
    def test_post(self):
        start = datetime.datetime(2012, 1, 1)
        end = datetime.datetime(2012, 2, 1)
        dos = models.DOS(userinfo=users.get_current_user(),
                         dos_datetime=start,
                         dos_enddateime=end)
        dos.put()
        req = mock_common.MockRequest(method='POST',
                                      POST={'amt_due': 100,
                                            'dos_datetime_0':  start.date(),
                                            'dos_datetime_1_time': '12:00 am',
                                            'dos_endtime_time': '12:30 am'})

        calendar_views.calendar_update_dos(req, dos.get_id(), 2012, 10, 1)
        dos = models.DOS.get_by_id(dos.get_id())
        self.assertEqual(int(dos.amt_due), 100)

    def test_no_op(self):
        req = mock_common.MockRequest()
        http_response = calendar_views.calendar_update_dos(req, 100, 0, 0, 0)
        self.assertIsInstance(http_response, HttpResponseRedirect)


class Test_calendar_delete_dos(mock_common.MockAppEngineTest):
    def test_correct_dos(self):
        start = datetime.datetime(2012, 1, 1)
        end = datetime.datetime(2012, 2, 1)
        dos = models.DOS(userinfo=users.get_current_user(),
                         dos_datetime=start,
                         dos_enddateime=end)
        dos.put()
        dos_id = dos.get_id()
        req = mock_common.MockRequest()
        calendar_views.calendar_delete_dos(req, dos_id, 2012, 10, 1)
        dos = models.DOS.get_by_id(dos_id)
        self.assertFalse(dos)

    def test_invalid_dos(self):
        req = mock_common.MockRequest()
        http_response = calendar_views.calendar_delete_dos(req, 1000, 2012, 10,
                                                           1)
        self.assertEqual('/Mindwell/calendar/',
                         http_response['Location'])


class Test_calendar_cancel_all_series_dos(mock_common.MockAppEngineTest):
    def test_correct_dos(self):
        start = datetime.datetime(2012, 1, 1)
        end = datetime.datetime(2012, 2, 1)
        dos = models.DOS(userinfo=users.get_current_user(),
                         dos_datetime=start,
                         dos_enddateime=end,
                         dos_repeat='One Day')
        dos.put()
        dos_id = dos.get_id()
        req = mock_common.MockRequest()
        calendar_views.calendar_cancel_all_series_dos(req, dos_id, 2012, 10, 1)
        dos = models.DOS.get_by_id(dos_id)
        self.assertEqual(dos.dos_repeat, 'No')

    def test_invalid_dos(self):
        req = mock_common.MockRequest()
        http_response = calendar_views.calendar_cancel_all_series_dos(
            req, 1000, 2012, 10, 1)
        self.assertEqual('/Mindwell/calendar/',
                         http_response['Location'])
