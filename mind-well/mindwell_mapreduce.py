from Mindwell.Client.models import *
import logging
from google.appengine.api import users
from mapreduce import operation as op

def process_DOS(entity):
    yield op.db.Put(entity)


def change_email(entity):  
  if entity.userinfo.email() == 'sara@healingllc.com':
      entity.userinfo = users.User('sara@healingllc.com')
      entity.put()