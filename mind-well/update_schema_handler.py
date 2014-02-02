import sys
sys.path.insert(0, 'reportlab.zip')
import logging
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Mindwell.settings'
import webapp2
from Mindwell.Client import update_schema
from google.appengine.ext import deferred

import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch

from google.appengine.ext import ereporter

ereporter.register_logger()


def log_exception(*args, **kwds):
    logging.error('Exception in request:')

# Log errors.
django.dispatch.Signal.connect(
    django.core.signals.got_request_exception, log_exception)

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
    django.core.signals.got_request_exception,
    django.db._rollback_on_exception)

class UpdateDOSHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(update_schema.UpdateDOSSchema)
        self.response.out.write('DOS Schema migration successfully initiated.')

app = webapp2.WSGIApplication([('/update_schema/dos', UpdateDOSHandler)])
