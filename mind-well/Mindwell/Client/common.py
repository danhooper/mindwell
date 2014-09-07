from google.appengine.ext import db
import models


def get_maximum_num_dos_fetch():
    return 3000


def delete_client(client):
    db.delete(models.DOS.safe_all().filter(
        "clientinfo =", client.key()).fetch(
        get_maximum_num_dos_fetch()))
    db.delete(models.Invoice.safe_all().filter(
        "clientinfo =", client.key()).fetch(
        get_maximum_num_dos_fetch()))
    client.delete()
    return True
