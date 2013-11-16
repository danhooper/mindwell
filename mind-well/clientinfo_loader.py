# Call like so:
#appcfg.py download_data --config_file=clientinfo_loader.py --filename=clientinfo_archive.csv --kind=ClientInfo --url=http://localhost:8080/remote_api c:\code\mindwell\branches\appengine\mind-well
#
import os, sys
# Force sys.path to have our own directory first, in case we want to import
# from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ['USER_EMAIL'] = 'test@example.com'

from google.appengine.ext import db
from google.appengine.tools import bulkloader
from Mindwell.Client.models import ClientInfo, UserInfo
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Mindwell.Client.secret_info import secret_passphrase


def decrypt(data, userid):
    if data is None:
        return None
    sha = SHA256.new()
    sha.update(UserInfo.GetUserRandomNumber(userid))
    sha.update(secret_passphrase)
    alg = AES.new(sha.digest(), AES.MODE_ECB)
    dec_res = alg.decrypt(data)
    dec_res = dec_res.rstrip('^')
    return dec_res

def userinfo_output(userinfo):
    return userinfo.user_id()

class ClientInfoExporter(bulkloader.Exporter):
    def __init__(self):
        self.properties = [
            ('userinfo', userinfo_output, None),
            ('lastname', decrypt, None),
            ('firstname', decrypt, None),
            ('cellnumber', decrypt, None),
            ('cellmessage', str, None),
            ('homenumber', decrypt, None),
            ('homemessage', str, None),
            ('worknumber', decrypt, None),
            ('workmessage', str, None),
            ('emailaddress', decrypt, None),
            ('address', decrypt, None),
            ('address2', decrypt, None),
            ('city', decrypt, None),
            ('state', str, None),
            ('zipcode', decrypt, None),
            ('dob_month', str, None),
            ('dob_day', decrypt, None),
            ('dob_year', decrypt, None),
            ('referrer', decrypt, None),
            ('client_status', str, None),
        ]
        bulkloader.Exporter.__init__(self, 'ClientInfo', self.properties)

    def output_entities(self, entity_generator):
        output_file = open(self.output_filename, 'w')
        for entity in entity_generator:
            for name, fn, default in self.properties:
                if fn == decrypt:
                    output_file.write(fn(entity[name], entity['userinfo'].user_id()))
                else:
                    output_file.write(fn(entity[name]))
                output_file.write(',',)
            output_file.write('\n')

exporters = [ClientInfoExporter]