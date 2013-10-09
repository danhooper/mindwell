import datetime
from Mindwell.Client import models
from django.test.utils import setup_test_environment
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed
import mock_common

setup_test_environment()


class Test_DOS(mock_common.MockAppEngineTest):

    def test_absolute_urls(self):
        self.assertRegexpMatches(self.dos.get_absolute_url(),
                                 '/Mindwell/\d+/update_dos/')
        self.assertRegexpMatches(self.dos.get_receipt_absolute_url(),
                                 '/Mindwell/\d+/dos_receipt/')
        self.assertRegexpMatches(
            self.dos.get_calendar_absolute_url(),
            '/Mindwell/2012/01/01/00/00/\d+/calendar_dos/')
        self.assertRegexpMatches(
            self.dos.get_update_absolute_url(),
            '/Mindwell/2012/01/01/\d+/calendar/')
        self.assertRegexpMatches(
            self.dos.get_delete_absolute_url(),
            '/Mindwell/2012/01/01/\d+/calendar_delete_dos/')
        self.assertRegexpMatches(
            self.dos.get_cancel_all_series_url(self.dos_start_datetime),
            '/Mindwell/2012/01/01/\d+/calendar_cancel_all_series_dos/')

    def test_dos_fields(self):
        self.assertEqual('fake lastname, fake firstname',
                         self.dos.__unicode__())
        self.assertEqual('01/01/2012', self.dos.get_dos_date_display())
        self.assertTrue(self.dos.getallfields_inc_hidden())
        self.assertTrue(self.dos.getallfields())
        self.assertTrue(self.dos.get_hover_tip())
        self.assertEqual((self.dos_start_datetime +
                          datetime.timedelta(minutes=45)),
                         self.dos.get_endtime())
        self.assertEqual(self.dos.get_repeat_end_date(),
                         datetime.datetime(2100, 12, 31, 0, 0))
        self.assertEqual('scheduleClient', self.dos.get_class_name())
        self.assertEqual('', self.dos.get_note())
        self.assertEqual(0, self.dos.get_repeat_freq())
        self.assertFalse(self.dos.get_blocked_time())
        self.assertEqual(1, self.dos.get_clientinfo_key())
        self.assertEqual('45', self.dos.get_duration())
        self.assertEqual('yellow', self.dos.get_background_color())
        self.assertEqual('blue', self.dos.get_text_color())

    def test_missing_clientinfo(self):
        clientinfo = models.ClientInfo()
        clientinfo.put()
        dos = models.DOS(dos_datetime=self.dos_start_datetime,
                         clientinfo=clientinfo)
        dos.put()
        db.delete(clientinfo)
        dos = models.DOS.get_by_id(dos.get_id())
        self.assertTrue(dos.get_blocked_time())
        self.assertFalse(dos.get_clientinfo_key())
        self.assertTrue(dos.getallfields_inc_hidden())
        self.assertFalse(unicode(dos))
        self.assertTrue(dos.get_class_name())
        self.assertTrue(dos.get_background_color())
        self.assertTrue(dos.get_text_color())


class Test_DOSRecurr(mock_common.MockAppEngineTest):
    def setUp(self):
        super(Test_DOSRecurr, self).setUp()
        self.dosrecurr = models.DOSRecurr(
            dos_base=self.dos, dos_recurr_datetime=self.dos_start_datetime)

    def test_absolute_urls(self):
        self.assertEqual(
            ('/Mindwell/2012/01/01/00/00/%d/calendar_dos_recurr/' %
             self.dos.get_id()),
            self.dosrecurr.get_calendar_absolute_url())

