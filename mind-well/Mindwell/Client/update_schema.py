import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Mindwell.settings'
import logging
import models
from google.appengine.ext import deferred
from google.appengine.ext import db

BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

def UpdateDOSSchema(cursor=None, num_updated=0):
    query = models.DOS.all()
    if cursor:
        query.with_cursor(cursor)

    to_put = []
    fetched_dos = False
    for dos in query.fetch(limit=BATCH_SIZE):
        fetched_dos = True
        if dos.meta_version == models.dos_meta_version and dos.user_id:
            continue
        dos.meta_version = models.dos_meta_version
        if not dos.user_id:
            dos.user_id = dos.userinfo.user_id()
        to_put.append(dos)

    if to_put:
        db.put(to_put)
        num_updated += len(to_put)
        logging.info(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
    if fetched_dos:
        deferred.defer(
            UpdateDOSSchema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.info(
            'UpdateDOSSchema complete with %d updates!', num_updated)
