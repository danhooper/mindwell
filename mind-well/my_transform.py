import codecs
from google.appengine.ext import db
from Mindwell.Client.secret_info import secret_passphrase
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os

def import_transform_encrypted(value):
    if value is None:
        return None
    hex_decoder = codecs.getdecoder('hex')
    return db.ByteString(hex_decoder(value)[0])

def export_transform_encrypted(value):
    if value is None:
        return u''
    ascii_text = str(value).encode('hex')
    return unicode(ascii_text)

def user_property(value):
    return value.email()


class EncryptedField():

    def __GetSHADigest(self, random_number = None):
        """ This function returns a sha hash of the user's random number
            and the secret password."""
        sha = SHA256.new()
        if not random_number:
            random_number = os.urandom(16)
        # mix in a random number
        sha.update(random_number)
        # mix in our secret password
        sha.update(secret_passphrase)
        return (sha.digest(), random_number)


    def encrypt(self, data):
        """Encrypts the data to be stored in the datastore"""
        if data is None:
            return None
        if data == 'None':
            return None
        if len(data) == 0:
            return None
        # need to pad the data so it is 16 bytes long for encryption
        mod_res = len(data) % 16
        if mod_res != 0:
            for i in range(0, 16 - mod_res):
                #pad the data with ^ (hopefully no one uses that as the last
                #charachter, if so it will be deleted
                data += '^'
        (sha_digest, random_number) = self.__GetSHADigest()
        alg = AES.new(sha_digest, AES.MODE_ECB)
        result = random_number + alg.encrypt(data)
        # encode the data as hex to store in a string
        # the result will otherwise have charchters that cannot be displayed
        ascii_text = str(result).encode('hex')
        return unicode(ascii_text)

def import_transform_encrypt(value):
    enc_field = EncryptedField()
    return enc_field.encrypt(value)
