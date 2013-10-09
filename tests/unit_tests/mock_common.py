import datetime
import unittest
from google.appengine.api import users
from google.appengine.ext import testbed
from Mindwell.Client import models


class MockRequest(object):
    def __init__(self, method='GET', COOKIES={}, META={}, POST={}, GET={}):
        self.method = method
        self.COOKIES = COOKIES
        self.META = META
        self.POST = POST
        self.GET = GET
        self.path = '/'


@staticmethod
def static_mock_return_true(*args, **kwargs):
    return True

default_user_email = 'test@example.com'
secondary_user = 'test2@example.com'


class MockAppEngineTest(unittest.TestCase):
    def setUp(self):
        super(MockAppEngineTest, self).setUp()
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.setup_env(USER_EMAIL=default_user_email,
                               USER_ID='123',
                               AUTH_DOMAIN='testbed',
                               APPLICATION_ID='testbed-test',
                               overwrite=True)
        self.testbed.init_user_stub()
        self.client = models.ClientInfo(userinfo=users.get_current_user(),
                                   lastname='fake lastname',
                                   firstname='fake firstname')
        self.client.put()
        self.dos_start_datetime = datetime.datetime(2012, 1, 1)
        self.dos = models.DOS(userinfo=users.get_current_user(),
                              clientinfo=self.client,
                              dos_datetime=self.dos_start_datetime)
        self.dos.put()
        self.secondary_userinfo = models.UserInfo(
            user_email_address=secondary_user, userid='124')
        self.secondary_userinfo.put()
        self.user_permission = models.UserPermission(
            userinfo=users.get_current_user(),
            permitteduser=users.User(secondary_user),
            permissionlevel='Read and Write',
            user_approved='Approved')
        self.user_permission.put()

    def tearDown(self):
        super(MockAppEngineTest, self).tearDown()
#        self.client.delete()
#        self.dos.delete()
#        self.secondary_userinfo.delete()
#        self.user_permission.delete()
        self.testbed.deactivate()
