import os
import codecs
import logging
import datetime
import common
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache
import extrawidgets
from django.forms.extras import SelectDateWidget
from django.core.urlresolvers import reverse
from django import forms
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from secret_info import secret_passphrase


class Checkbox(object):
    def __init__(self, choice, selected):
        self.choice = choice
        self.selected = selected

    def __unicode__(self):
        return self.choice


def pull_current_user_id_from_request(request):
    """Gets the current user, which might either be the logged in user
        or the user they are acting as."""
    # first use the logged in user
    current_user = users.get_current_user().user_id()
    if request is not None:
        if 'current_user' in request.COOKIES:
            current_user = UserPermission().safe_get(
                str(request.COOKIES['current_user']))
            if current_user is not None:
                return current_user.permitted_user_id
    return current_user


def date_formatter(date_in):
    """Converts a date to Mon/Day/Year, xx/xx/xxxx"""
    return unicode(date_in.strftime('%m/%d/%Y'))


def global_get_all(classname, request=None, keys_only=False):
    """This replaces the all functions from google app engine on models.
        This function will filter out all entities that a user owns
        so that no user can see someone else's information."""
    result = classname.all(keys_only=keys_only)
    current_user_id = pull_current_user_id_from_request(request)
    return result.filter('user_id =', current_user_id)


def global_get_by_id(classname, ids, request=None, parent=None):
    """This replaces the get_by_id of google app engine on models.
       This function ensures that a user can only access entities they
       own."""
    result = classname.get_by_id(int(ids), parent)
    if result is None:
        result = classname.get_by_key_name(str(ids), parent)
    if result is None:
        logging.info('could not find %s with id %s', classname, ids)
        return None
    current_user_id = pull_current_user_id_from_request(request)
    if result.user_id != current_user_id:
        logging.info('current_user id is not the same as the result user id')
        return None
    return result


# TODO: need to handle multiple keys
def global_get(classname, keys):
    """This replaces the app engine get function for entities.
       It ensures that a given user can only access their own
       entities."""
    try:
        result = classname.get(keys)
        if result.user_id != users.get_current_user().user_id():
            return None
        return result
    except (db.KindError, AttributeError):
        return None


class EncryptedField(db.StringProperty):
    """ This supports a property which is encrypted with a salted hash.  See
        http://danhooper.blogspot.com/2010/06/encrypting-fields-in-google-app-engine.html
        for more information."""
    data_type = str

    def __get_sha_digest(self, random_number=None):
        """ This function returns a sha hash of a random number
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
        # need to pad the data so it is 16 bytes long for encryption
        mod_res = len(data) % 16
        if mod_res != 0:
            for unused_i in range(0, 16 - mod_res):
                #pad the data with ^ (hopefully no one uses that as the last
                #charachter, if so it will be deleted
                data += '^'
        (sha_digest, random_number) = self.__get_sha_digest()
        alg = AES.new(sha_digest, AES.MODE_ECB)
        result = random_number + alg.encrypt(data)
        # encode the data as hex to store in a string
        # the result will otherwise have charachters that cannot be displayed
        ascii_text = str(result).encode('hex')
        return unicode(ascii_text)

    def decrypt(self, data):
        """ Decrypts the data from the datastore.  Basically the inverse of
            encrypt."""
        # check that either the string is None or the data itself is none
        if data is None:
            return None
        if data == 'None':
            return None
        hex_decoder = codecs.getdecoder('hex')
        hex_decoded_res = hex_decoder(data)[0]
        random_number = hex_decoded_res[0:16]
        (sha_digest, random_number) = self.__get_sha_digest(random_number)
        alg = AES.new(sha_digest, AES.MODE_ECB)
        dec_res = alg.decrypt(hex_decoded_res[16:])
        #remove the ^ from the strings in case of padding
        return unicode(dec_res.rstrip('^'))

    def get_value_for_datastore(self, model_instance):
        """ For writing to datastore """
        data = super(EncryptedField,
                     self).get_value_for_datastore(model_instance)
        enc_res = self.encrypt(data)
        if enc_res is None:
            return None
        return str(enc_res)

    def make_value_from_datastore(self, value):
        """ For reading from datastore. """
        if value is not None:
            return str(self.decrypt(value))
        return ''

    def validate(self, value):
        if isinstance(value, unicode):
            value = str(value)
        if value is not None and not isinstance(value, str):
            raise db.BadValueError('Property %s must be convertible '
                                'to a str instance (%s)' %
                                (self.name, value))
        return super(EncryptedField, self).validate(value)

    def empty(self, value):
        return not value


class UserInfo(db.Model):
    """ This class is used to save information about permitted users."""

    user_email_address = db.StringProperty()
    user_id = db.StringProperty(default=None)

    @staticmethod
    def CurrentUserAllowed():
        """ This function returns true if the current user is allowed access
            this application."""
        current_user = users.get_current_user()
        if not current_user:
            return False
        userlist = memcache.get("userlist")
        if userlist is not None:
            pass
        else:
            userlist = UserInfo.all().fetch(common.get_maximum_num_dos_fetch())
            memcache.add("userlist", userlist)
        for user in userlist:
            if user.user_email_address == current_user.email().lower():
                if not user.user_id:
                    userlist = UserInfo.all().filter(
                        'user_email_address =', current_user.email().lower())
                    user = userlist.get()
                    if user is not None:
                        if not user.user_id:
                            user.user_id = current_user.user_id()
                            user.put()
                            logging.info('Adding user id %s' % (
                                str(current_user.user_id())))
                    memcache.delete("userlist")
                    return True
            if user.user_id == current_user.user_id():
                return True
        logging.info('user %s tried to login' % current_user.email())
        return False

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)


class UserPermission(db.Model):
    """ This class is used to hold information about which users may act on
        behalf of other uses (can see their client etc)."""

    userinfo = db.UserProperty()  # this is the user with the permission
    # Not used today, but in the future will be filtered all the time to get a
    # user's Clients
    user_id = db.StringProperty()
    user_email = db.StringProperty()
    # this is the user the current user can act on behalf of
    #permitteduser = db.UserProperty()
    permitted_user_email = db.StringProperty()
    permitted_user_id = db.StringProperty()
    PERMISSION_LEVEL_CHOICES = (
        'Read and Write',
        )
    permissionlevel = db.StringProperty(verbose_name='Permission Level',
        choices=PERMISSION_LEVEL_CHOICES, default='Read and Write')
    user_approved = db.StringProperty(verbose_name='User Approval',
                                      default='Not Yet Approved')

    @staticmethod
    def safe_all(request=None, keys_only=False):
        """ This function is used to get all the entities of this class that
            the current user owns."""
        return global_get_all(UserPermission, request=request,
                              keys_only=keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        """ This function is used to get a specific entity of this class that
            the current user owns."""
        return global_get_by_id(UserPermission, ids, request=request,
                                parent=None)

    @staticmethod
    def safe_get(keys):
        """ This function is used to get a specific entity of this class that
            the current user owns."""
        user_permission = global_get(UserPermission, keys)
        if user_permission:
            if user_permission.user_approved == 'Approved':
                return user_permission
        return None

    @staticmethod
    def get_permission_requests():
        return UserPermission.all().filter('permitted_user_email = ',
                                           users.get_current_user().email())

    @staticmethod
    def unsafe_get(ids, parent=None):
        """ Since ."""
        result = UserPermission.get_by_id(int(ids), parent)
        if result is None:
            result = UserPermission.get_by_key_name(str(ids), parent)
        if result is None:
            return None
        return result

    def get_absolute_url(self):
        return reverse('update_permission_requests',
                       kwargs={'request_permission_id':
                               str(self.key().id_or_name())})

    def get_delete_absolute_url(self):
        return reverse('delete_permission',
                       kwargs={'permission_id': str(self.key().id_or_name())})

    def get_id(self):
        return str(self.key().id_or_name())

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)


class UserPermissionForm(forms.Form):
    """ Creates the userpermission form for requesters to use.
        Omits the user_approved field."""

    # this is the user the current user can act on behalf of
    permitted_user_email = forms.CharField(max_length=200)
    PERMISSION_LEVEL_CHOICES = (
        ('Read and Write', 'Read and Write'),
        )
    permissionlevel = forms.ChoiceField(label='Permission Level',
                                        choices=PERMISSION_LEVEL_CHOICES)

    # Force the user email to be lower case
    def clean_permitted_user_email(self):
        data = self.cleaned_data['permitted_user_email']
        if data:
            data = str(data).lower()
        return data


class UserPermissionRequestsForm(forms.Form):
    """ Creates the userpermission form for approvers/rejectors to use.
        Creates the userpermission form but omits the submitter's fields.  So
        this is used when the user is approving or rejecting other requester's
        permission requests."""

    USER_APPROVED_CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Not Yet Approved', 'Not Yet Approved'),
    )
    user_approved = forms.ChoiceField(label='User Approval',
        choices=USER_APPROVED_CHOICES)


client_info_meta_version = '1'


class ClientInfo(db.Model):
    """ Holds information about clients, such as names and addresses."""
    # Filtered all the time to get auser's Clients
    userinfo = db.UserProperty()
    # Not used today, but in the future will be filtered all the time to get a
    # user's Clients
    user_id = db.StringProperty()
    # Used to make updates to model over time
    meta_version = db.StringProperty(default=client_info_meta_version)
    create_time = db.DateTimeProperty(auto_now_add=True, indexed=False)
    lastname = EncryptedField(verbose_name='last name', indexed=False)
    firstname = EncryptedField(verbose_name='First Name', indexed=False)
    MESSAGE_CHOICES = (
        'Message OK',
        'Message Not OK'
        )
    cellnumber = EncryptedField(verbose_name='Cell Number', indexed=False)
    cellmessage = db.StringProperty(verbose_name='Cell Message',
        choices=MESSAGE_CHOICES, default='Message Not OK', indexed=False)
    homenumber = EncryptedField(verbose_name='Home Number')
    homemessage = db.StringProperty(verbose_name='Home Message',
        choices=MESSAGE_CHOICES, default='Message Not OK', indexed=False)
    worknumber = EncryptedField(verbose_name='Work Number', indexed=False)
    workmessage = db.StringProperty(verbose_name='Work Message',
        choices=MESSAGE_CHOICES, default='Message Not OK', indexed=False)
    emailaddress = EncryptedField(verbose_name='Email', indexed=False)
    address = EncryptedField(verbose_name='Address', indexed=False)
    address2 = EncryptedField(verbose_name='Address 2', indexed=False)
    city = EncryptedField(verbose_name='City', indexed=False)
    STATE_CHOICES = (
        'Alabama',
        'Alaska',
        'Alabama',
        'Alabama',
        'Alabama',
        'Colorado',
        'Connecticut',
        'Delaware',
        'Florida',
        'Georgia',
        'Hawaii',
        'Idaho',
        'Illinois',
        'Indiana',
        'Iowa',
        'Kansas',
        'Kentucky',
        'Louisiana',
        'Maine',
        'Maryland',
        'Massachusetts',
        'Michigan',
        'Minnesota',
        'Mississippi',
        'Missouri',
        'Montana',
        'Nebraska',
        'Nevada',
        'New Hampshire',
        'New Jersey',
        'New Mexico',
        'New York',
        'North Carolina',
        'North Dakota',
        'Ohio',
        'Oklahoma',
        'Oregon',
        'Pennsylvania',
        'Rhode Island',
        'South Carolina',
        'South Dakota',
        'Tennessee',
        'Texas',
        'Utah',
        'Vermont',
        'Virginia',
        'Washington',
        'Washington DC',
        'West Virginia',
        'Wisconsin',
        'Wyoming',
        )
    state = db.StringProperty(verbose_name='State', choices=STATE_CHOICES,
                              default='Maryland', indexed=False)
    zipcode = EncryptedField(verbose_name='Zip Code', indexed=False)
    dob = db.DateProperty(verbose_name='dob', indexed=False)

    guardians_name = EncryptedField(verbose_name='Guardians Name',
                                    indexed=False)
    guardians_phone_number = EncryptedField(verbose_name='Guardians Phone Number',
                                            indexed=False)
    emergency_contact = EncryptedField(verbose_name='Emergency Contact',
                                       indexed=False)
    emergency_contact_phone_number = EncryptedField(verbose_name='Emergency Contact Phone Number', indexed=False)
    #Indexed for autocomplete of referrer
    referrer = EncryptedField(verbose_name='Referrered By')
    #Indexed for autocomplete of DSM code
    dsm_code = db.StringProperty(verbose_name='dsm Code')
    CLIENT_STATUS_CHOICES = (
        'Active',
        'Inactive',
        )
    reason_for_visit = db.StringProperty(default='',
                                         verbose_name="Reason for Visit")
    client_status = db.StringProperty(verbose_name='Client Status',
                                      choices=CLIENT_STATUS_CHOICES,
                                      default='Active')

    def __unicode__(self):
        """ Converts the user to a unicode string."""
        return  u'%s, %s' % (self.lastname, self.firstname)

    def get_absolute_url(self):
        """ Link in MindWell to show a specific client."""
        return reverse('show_specific_client',
                       kwargs={'client_id': str(self.key().id_or_name())})

    def get_update_url(self):
        """ Link in MindWell to modify a specific client."""
        return reverse('update_client',
                       kwargs={'client_id': str(self.key().id_or_name())})

    def get_delete_url(self):
        """ Link in MindWell to delete a specific client."""
        return reverse('delete_client',
                       kwargs={'client_id': str(self.key().id_or_name())})



    def getallfields_inc_hidden(self):
        """ Gets all the fields for the client including hidden ones."""
        return (
            ('Client ID', self.get_id()),
            ('Last Name', self.lastname),
            ('First Name', self.firstname),
            ('Cell Number', self.cellnumber),
            ('Cell Message', self.cellmessage),
            ('Home Number', self.homenumber),
            ('Home Message', self.homemessage),
            ('Work Number', self.worknumber),
            ('Work Message', self.workmessage),
            ('Email', self.emailaddress),
            ('Address', self.address),
            ('Address 2', self.address2),
            ('City', self.city),
            ('State', self.state),
            ('Zip Code', self.zipcode),
            ('DOB', self.dob),
            ('Referrer', self.referrer),
            ('DSM Code', self.dsm_code),
            ('Client Status', self.client_status),
            ('Guardians Name', self.guardians_name),
            ('Guardians Phone Number', self.guardians_phone_number),
            ('Emergency Contact', self.emergency_contact),
            ('Emergency Contact Phone Number',
             self.emergency_contact_phone_number),
            ('Reason for Visit', self.reason_for_visit)
        )

    def getallfields(self):
        """ Gets all the fields for the client excluding hidden ones."""
        return (
            ('Last Name', self.lastname),
            ('First Name', self.firstname),
            ('Cell Number', self.cellnumber),
            ('Cell Message', self.cellmessage),
            ('Home Number', self.homenumber),
            ('Home Message', self.homemessage),
            ('Work Number', self.worknumber),
            ('Work Message', self.workmessage),
            ('Email', self.emailaddress),
            ('Address', self.address),
            ('Address 2', self.address2),
            ('City', self.city),
            ('State', self.state),
            ('Zip Code', self.zipcode),
            ('DOB', self.dob),
            ('Referrer', self.referrer),
            ('DSM Code', self.dsm_code),
            ('Client Status', self.client_status),
            ('Guardians Name', self.guardians_name),
            ('Guardians Phone Number', self.guardians_phone_number),
            ('Emergency Contact', self.emergency_contact),
            ('Emergency Contact Phone Number',
             self.emergency_contact_phone_number),
            ('Reason for Visit', self.reason_for_visit)
        )

    def get_contact_fields(self):
        """ Gets all the contact information fields for the client."""
        return (
            ('Cell Number', self.cellnumber),
            ('Cell Message', self.cellmessage),
            ('Home Number', self.homenumber),
            ('Home Message', self.homemessage),
            ('Work Number', self.worknumber),
            ('Work Message', self.workmessage),
            ('Email', self.emailaddress),
            )

    def get_address_fields(self):
        """ Gets all the address information fields for the client."""
        return (
            ('Address', self.address),
            ('Address 2', self.address2),
            ('City', self.city),
            ('State', self.state),
            ('Zip Code', self.zipcode),
            )

    def get_other_fields(self):
        """ Gets all the other fields for the client."""
        return (
            ('DOB', self.dob),
            ('DSM Code', self.dsm_code),
            ('Client Status', self.client_status),
            ('Referrer', self.referrer),
            ('Guardians Name', self.guardians_name),
            ('Guardians Phone Number', self.guardians_phone_number),
            ('Emergency Contact', self.emergency_contact),
            ('Emergency Contact Phone Number',
             self.emergency_contact_phone_number),
            ('Reason for Visit', self.reason_for_visit)
        )

    def get_hover_tip(self):
        """ Gets all the fields separated by <br/>."""
        hover = ''
        for field in self.getallfields():
            hover += unicode(field[0]) + ':' + unicode(field[1]) + '<br/>'
        return hover

    def get_id(self):
        """ Gets the clients key by id or name."""
        return self.key().id_or_name()

    @staticmethod
    def safe_all(request=None, keys_only=False):
        """ Used to get all the clients for a given user."""
        return global_get_all(ClientInfo, request=request, keys_only=keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        """ Used to get clients by id for a given user."""
        return global_get_by_id(ClientInfo, ids, request=request, parent=None)

    @staticmethod
    def get_clientinfo_choices(request=None):
        choices = [['', ' '], ]
        if request:
            clients = ClientInfo.safe_all(request)
        else:
            clients = ClientInfo.safe_all()
        clients = clients.filter('client_status =', 'Active')
        choices.extend([(client.get_id(), client) for client in clients])
        return choices

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)

    class Meta:
        ordering = ["lastname"]


class ClientForm(forms.Form):
    """ Form used to add or update a client.  The userinfo is populated
        manually after creating the client. """
    lastname = forms.CharField(max_length=300, required=False)
    firstname = forms.CharField(max_length=300, required=False)
    MESSAGE_CHOICES = (
        ('Message Not OK', 'Message Not OK'),
        ('Message OK', 'Message OK'),
        )
    cellnumber = forms.CharField(max_length=300, required=False)
    cellmessage = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)
    homenumber = forms.CharField(max_length=300, required=False)
    homemessage = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)
    worknumber = forms.CharField(max_length=300, required=False)
    workmessage = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)
    emailaddress = forms.CharField(max_length=300, required=False)
    address = forms.CharField(max_length=300, required=False)
    address2 = forms.CharField(max_length=300, required=False)
    city = forms.CharField(max_length=300, required=False)
    STATE_CHOICES = (
        ('Alabama', 'Alabama'),
        ('Alaska', 'Alaska'),
        ('Alabama', 'Alabama'),
        ('Alabama', 'Alabama'),
        ('Alabama', 'Alabama'),
        ('Colorado', 'Colorado'),
        ('Connecticut', 'Connecticut'),
        ('Delaware', 'Delaware'),
        ('Florida', 'Florida'),
        ('Georgia', 'Georgia'),
        ('Hawaii', 'Hawaii'),
        ('Idaho', 'Idaho'),
        ('Illinois', 'Illinois'),
        ('Indiana', 'Indiana'),
        ('Iowa', 'Iowa'),
        ('Kansas', 'Kansas'),
        ('Kentucky', 'Kentucky'),
        ('Louisiana', 'Louisiana'),
        ('Maine', 'Maine'),
        ('Maryland', 'Maryland'),
        ('Massachusetts', 'Massachusetts'),
        ('Michigan', 'Michigan'),
        ('Minnesota', 'Minnesota'),
        ('Mississippi', 'Mississippi'),
        ('Missouri', 'Missouri'),
        ('Montana', 'Montana'),
        ('Nebraska', 'Nebraska'),
        ('Nevada', 'Nevada'),
        ('New Hampshire', 'New Hampshire'),
        ('New Jersey', 'New Jersey'),
        ('New Mexico', 'New Mexico'),
        ('New York', 'New York'),
        ('North Carolina', 'North Carolina'),
        ('North Dakota', 'North Dakota'),
        ('Ohio', 'Ohio'),
        ('Oklahoma', 'Oklahoma'),
        ('Oregon', 'Oregon'),
        ('Pennsylvania', 'Pennsylvania'),
        ('Rhode Island', 'Rhode Island'),
        ('South Carolina', 'South Carolina'),
        ('South Dakota', 'South Dakota'),
        ('Tennessee', 'Tennessee'),
        ('Texas', 'Texas'),
        ('Utah', 'Utah'),
        ('Vermont', 'Vermont'),
        ('Virginia', 'Virginia'),
        ('Washington', 'Washington'),
        ('Washington DC', 'Washington DC'),
        ('West Virginia', 'West Virginia'),
        ('Wisconsin', 'Wisconsin'),
        ('Wyoming', 'Wyoming'),
        )
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False,
                              initial='Maryland')
    zipcode = forms.CharField(max_length=300, required=False)
    this_year = datetime.date.today().year
    years = range(this_year - 100, this_year + 2)
    dob = forms.DateField(required=False,
                          widget=SelectDateWidget(years=years, required=False))

    guardians_name = forms.CharField(max_length=300, required=False)
    guardians_phone_number = forms.CharField(max_length=300, required=False)
    emergency_contact = forms.CharField(max_length=300, required=False)
    emergency_contact_phone_number = forms.CharField(max_length=300,
                                                     required=False)
    #Indexed for autocomplete of referrer
    referrer = forms.CharField(max_length=300, required=False)
    #Indexed for autocomplete of DSM code
    dsm_code = forms.CharField(max_length=300, required=False)
    reason_for_visit = forms.CharField(max_length=300, required=False)
    CLIENT_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        )
    client_status = forms.ChoiceField(choices=CLIENT_STATUS_CHOICES,
                                      required=False)


class SimpleClientForm(forms.Form):
    """ Form used to add or update a client.  The userinfo is populated
        manually after creating the client. """
    lastname = forms.CharField(max_length=300, required=False,
                               label='Last name')
    firstname = forms.CharField(max_length=300, required=False,
                                label='First name')
    MESSAGE_CHOICES = (
        ('Message Not OK', 'Message Not OK'),
        ('Message OK', 'Message OK'),
        )
    cellnumber = forms.CharField(max_length=300, required=False,
                                 label='Cell number')
    cellmessage = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False,
                                    label='Cell message')
    emailaddress = forms.CharField(max_length=300, required=False,
                                   label='Email')
    this_year = datetime.date.today().year
    years = range(this_year - 100, this_year + 2)
    dob = forms.DateField(required=False,
                          widget=SelectDateWidget(years=years, required=False))
    #Indexed for autocomplete of referrer
    referrer = forms.CharField(max_length=300, required=False,
                               label='Referred by')
    reason_for_visit = forms.CharField(max_length=300, required=False,
                                       label='Reason for visit')

dos_meta_version = '3'


class DOS(db.Model):
    """ Model for Date of Session (DOS). This basically stores information
        about a session with a client. """
    userinfo = db.UserProperty()
    user_id = db.StringProperty()
    meta_version = db.StringProperty(default=dos_meta_version)

    clientinfo = db.ReferenceProperty(ClientInfo)

    session_type = db.StringProperty(verbose_name='Session Type',
                                     default='',
                                     indexed=False)
    SESSION_RESULT_CHOICES = (
        'Scheduled',
        'Attended',
        'No Show',
        'Cancellation - Late',
        'Cancellation - Timely',
        'Payment Received',
        )
    # Used to filter DOS based upon attended DOS
    session_result = db.StringProperty(verbose_name='Session Result',
                                       choices=SESSION_RESULT_CHOICES,
                                       default='Scheduled')
    # Used to get the autocomplete field for dsm codes
    dsm_code = db.StringProperty(verbose_name='DSM Code')
    type_pay = db.StringProperty(verbose_name='Type Of Payment', indexed=False)
    amt_due = db.StringProperty(verbose_name='Amount Due', indexed=False)
    amt_paid = db.StringProperty(verbose_name='Amount Paid', indexed=False)
    note = db.StringProperty(verbose_name='Note', indexed=False)
    # Used to find DOS based upon start times
    dos_datetime = db.DateTimeProperty(verbose_name='DOS Date and Time')
    # Used to find DOS based upon end times
    dos_endtime = db.TimeProperty(verbose_name='DOS End Time')
    DURATION_CHOICES = (
        '0',
        '15',
        '30',
        '45',
        '60',
        '75',
        '90',
        '105',
        '120',
        )
    dos_duration = db.StringProperty(verbose_name='DOS Duration',
                                     choices=DURATION_CHOICES, default='45',
                                     indexed=False)
    REPEAT_CHOICES = (
        'No',
        'One Day',
        'One Week',
        'Two Weeks',
        'Three Weeks',
        'Four Weeks',
        )
    dos_repeat = db.StringProperty(verbose_name='DOS Repeat',
                                   choices=REPEAT_CHOICES, default='No')
    dos_repeat_end_date = db.DateProperty(verbose_name='Repeat End Date')

    def get_dos_date_display(self):
        """ Gets the dos date to display to the user. """
        return date_formatter(self.dos_datetime)

    def getallfields_inc_hidden(self):
        """ Gets all the dos fields including hidden ones. """
        client_id = 0
        if self.get_clientinfo():
            client_id = self.clientinfo.get_id()
        return (
            ('DOS ID', self.get_id()),
            ('Client ID', client_id),
            ('Session Type', self.session_type),
            ('Session Result', self.session_result),
            ('DSM Code', self.dsm_code),
            ('Type of Payment', self.type_pay),
            ('Amount Due', self.amt_due),
            ('Amount Paid', self.amt_paid),
            ('Note', self.note),
            ('DOS Date and Time', self.dos_datetime),
            ('DOS Repeat', self.dos_repeat),
            ('Repeat End Date', self.dos_repeat_end_date),
            )

    def getallfields(self):
        """ Gets all the dos fields excluding hidden ones. """
        return (
            ('Session Type', self.session_type),
            ('Session Result', self.session_result),
            ('DSM Code', self.dsm_code),
            ('Type of Payment', self.type_pay),
            ('Amount Due', self.amt_due),
            ('Amount Paid', self.amt_paid),
            ('Running Balance', 0),
            ('Note', self.note),
            ('DOS Date and Time', self.dos_datetime),
            ('DOS Repeat', self.dos_repeat),
            ('Repeat End Date', self.dos_repeat_end_date),
            )

    def get_hover_tip(self):
        """ Gets a hover tip for all the fields of a DOS. """
        hover = ''
        for field in self.getallfields():
            if field[0] == 'Running Balance':
                continue
            hover += unicode(field[0]) + ':' + unicode(field[1]) + '<br/>'
        return hover

    def get_absolute_url(self):
        """ Gets the update url of this DOS. """
        return reverse('update_dos', kwargs={'dos_id': str(self.get_id())})

    def get_receipt_absolute_url(self):
        """ Gets the url of this DOS's receipt. """
        return reverse('dos_receipt', kwargs={'dos_id': str(self.get_id())})

    def get_calendar_absolute_url(self):
        """ Gets the url of this DOS to show the form to update this DOS. """
        if self.dos_datetime:
            return reverse('calendar_dos',
                           args=('%04d' % self.dos_datetime.year,
                                 '%02d' % self.dos_datetime.month,
                                 '%02d' % self.dos_datetime.day,
                                 '%02d' % self.dos_datetime.hour,
                                 '%02d' % self.dos_datetime.minute,
                                 '%d' % int(self.get_id())))
        return self.get_absolute_url()

    def get_update_absolute_url(self):
        """ Gets the url of this DOS to make the update to it in the calendar
            view. """
        if self.dos_datetime:
            return reverse('calendar_update_dos',
                           args=('%04d' % self.dos_datetime.year,
                                 '%02d' % self.dos_datetime.month,
                                 '%02d' % self.dos_datetime.day,
                                 '%d' % int(self.get_id())))
        return self.get_absolute_url()

    def get_delete_absolute_url(self):
        """ Gets the url to delete this DOS. """
        if self.dos_datetime:
            return reverse('calendar_delete_dos',
                           args=('%04d' % self.dos_datetime.year,
                                 '%02d' % self.dos_datetime.month,
                                 '%02d' % self.dos_datetime.day,
                                 '%d' % int(self.get_id())))

    def get_cancel_all_series_url(self, dos_recurr_datetime):
        """ Gets the URL to cancel all repeating DOS'. """
        return reverse('calendar_cancel_all_series_dos',
                       args=('%04d' % dos_recurr_datetime.year,
                             '%02d' % dos_recurr_datetime.month,
                             '%02d' % dos_recurr_datetime.day,
                             '%d' % int(self.get_id())))

    def get_starttime(self):
        """ Gets the starting time of this DOS. """
        return self.dos_datetime

    def get_endtime(self):
        """ Gets the ending time of this DOS.
            Note: For old DOS this used to have a duration, now it has an
            explicit end time."""
        if self.dos_endtime:
            return datetime.datetime.combine(self.dos_datetime.date(),
                                             self.dos_endtime)
        try:
            if int(self.dos_duration) == 0:
                dos_duration = 15
            else:
                dos_duration = self.dos_duration
            end_time = (self.dos_datetime +
                        datetime.timedelta(minutes=int(dos_duration)))
            return end_time
        except TypeError:
            return self.dos_datetime + datetime.timedelta(minutes=15)

    def get_repeat_end_date(self):
        """ Gets the date that this DOS stops repeating.
            Note: There used to not be a specific end date, so we set the end
            date for those DOS' far in the future. """
        try:
            if self.dos_repeat_end_date is not None:
                return datetime.datetime.fromordinal(
                    self.dos_repeat_end_date.toordinal())
        except AttributeError:
            logging.info('get_repeat_end_date AttributeError')
        return datetime.datetime(2100, 12, 31, 0, 0)

    def get_id(self):
        """ Gets the ID or name of this DOS. """
        return self.key().id_or_name()

    def __unicode__(self):
        if self.get_clientinfo():
            uni = self.clientinfo.__unicode__()
        else:
            uni = ''
        return uni

    def get_clientinfo(self):
        try:
            return self.clientinfo
        except db.ReferencePropertyResolveError:
            logging.exception('Failed to get DOS clientinfo')
            return None

    def get_class_name(self):
        """ Gets the HTML class name of this DOS based upon attributes of this
            DOS. """
        try:
            if not self.get_clientinfo():
                return 'blocked_time'
            if self.session_result.lower().find('schedule') != -1:
                return 'scheduleClient'
            elif self.session_result.lower().find('no show') != -1:
                return 'noShow'
            elif self.session_result.lower().find('cancel') != -1:
                return 'cancel'
            else:
                return 'attendedClient'
        except AttributeError:
            return 'scheduleClient'

    def get_note(self):
        """ Gets the note for this DOS. """
        if self.note is not None:
            return self.note
        return u''

    def get_repeat_freq(self):
        """ Returns how often this DOS repeats in days."""
        if str(self.dos_repeat) == 'One Day':
            return 1
        if str(self.dos_repeat) == 'One Week':
            return 7
        if self.dos_repeat == 'Two Weeks':
            return 14
        if self.dos_repeat == 'Three Weeks':
            return 21
        if self.dos_repeat == 'Four Weeks':
            return 28
        return 0

    def get_blocked_time(self):
        """ True if this is a blocked time (no client, user just wants to
            block the time in the schedule)."""
        if self.get_clientinfo():
            return False
        else:
            return True

    def get_clientinfo_key(self):
        """ Gets the clientinfo key or an empty string if it isn't set. """
        if self.get_clientinfo():
            return self.clientinfo.get_id()
        return ''

    def get_duration(self):
        """ Gets the duration of this DOS in minutes. """
        if self.dos_endtime:
            end_minutes = self.dos_endtime.hour * 60 + self.dos_endtime.minute
            start_minutes = self.dos_datetime.time().hour * 60 + \
                self.dos_datetime.time().minute
            return (end_minutes - start_minutes)
        else:
            return self.dos_duration

    def get_background_color(self):
        """ Gets the background color of this DOS based upon various
            attributes. """
        try:
            if not self.get_clientinfo():
                return 'blue'
            if self.session_result.lower().find('schedule') != -1:
                return 'yellow'
            elif self.session_result.lower().find('no show') != -1:
                return 'red'
            elif self.session_result.lower().find('cancel') != -1:
                return 'gray'
            elif self.session_result.lower().find('received') != -1:
                return 'lightgreen'
            else:
                return 'green'
        except AttributeError:
            return 'yellow'

    def get_text_color(self):
        """ Gets the text color of this DOS based upon various attributes. """
        try:
            if not self.get_clientinfo():
                return 'white'
            if self.session_result.lower().find('schedule') != -1:
                return 'blue'
            elif self.session_result.lower().find('no show') != -1:
                return 'white'
            elif self.session_result.lower().find('cancel') != -1:
                return 'white'
            elif self.session_result.lower().find('received') != -1:
                return 'blue'
            else:
                return 'white'
        except AttributeError:
            return 'blue'

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)

    @staticmethod
    def safe_all(request=None, keys_only=False):
        """ Fetches all the DOS for a given user. """
        return global_get_all(DOS, request=request, keys_only=keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        """ Fetches the DOS by ID for a given user. """
        return global_get_by_id(DOS, ids, request=request, parent=None)


class DOSForm(forms.Form):
    """ Used to create a form for a DOS including the client drop down. """

    clientinfo = forms.ChoiceField(required=False)

    session_type = forms.CharField(max_length=300, required=False)
    SESSION_RESULT_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Attended', 'Attended'),
        ('No Show', 'No Show'),
        ('Cancellation - Late', 'Cancellation - Late'),
        ('Cancellation - Timely', 'Cancellation - Timely'),
        ('Payment Received', 'Payment Received'),
        )
    # Used to filter DOS based upon attended DOS
    session_result = forms.ChoiceField(choices=SESSION_RESULT_CHOICES,
                                       required=False)
    # Used to get the autocomplete field for dsm codes
    dsm_code = forms.CharField(max_length=300, required=False)
    type_pay = forms.CharField(max_length=300, required=False)
    amt_due = forms.CharField(max_length=300, required=False)
    amt_paid = forms.CharField(max_length=300, required=False)
    note = forms.CharField(max_length=300, required=False)
    # Used to find DOS based upon start times
    dos_datetime = forms.DateTimeField(
        widget=extrawidgets.SplitSelectDateTimeWidget(minute_step=15))
    # Used to find DOS based upon end times
    dos_endtime = forms.TimeField(
        widget=extrawidgets.SelectTimeWidget(minute_step=15))
    DURATION_CHOICES = (
        ('0', '0'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),
        ('60', '60'),
        ('75', '75'),
        ('90', '90'),
        ('105', '105'),
        )
    REPEAT_CHOICES = (
        ('No', 'No'),
        ('One Day', 'One Day'),
        ('One Week', 'One Week'),
        ('Two Weeks', 'Two Weeks'),
        ('Three Weeks', 'Three Weeks'),
        ('Four Weeks', 'Four Weeks'),
        )
    dos_repeat = forms.ChoiceField(choices=REPEAT_CHOICES, required=False)
    dos_repeat_end_date = forms.DateField(required=False)

    print_receipt = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['clientinfo'].choices = (
            ClientInfo.get_clientinfo_choices(kwargs.get('request')))
        if 'request' in kwargs:
            del kwargs['request']
        super(DOSForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'blocked_time',
                           forms.BooleanField(required=False))

    def get_all_fields(self):
        """ Gets all the fields for this form. """
        return str(dir(self))


class DOSFormNoClientSelect(forms.Form):
    """ Used to create a form for a DOS without showing the client drop
        down. """


    session_type = forms.CharField(max_length=300, required=False)
    SESSION_RESULT_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Attended', 'Attended'),
        ('No Show', 'No Show'),
        ('Cancellation - Late', 'Cancellation - Late'),
        ('Cancellation - Timely', 'Cancellation - Timely'),
        ('Payment Received', 'Payment Received'),
        )
    # Used to filter DOS based upon attended DOS
    session_result = forms.ChoiceField(choices=SESSION_RESULT_CHOICES,
                                       required=False)
    # Used to get the autocomplete field for dsm codes
    dsm_code = forms.CharField(max_length=300, required=False)
    type_pay = forms.CharField(max_length=300, required=False)
    amt_due = forms.CharField(max_length=300, required=False)
    amt_paid = forms.CharField(max_length=300, required=False)
    note = forms.CharField(max_length=300, required=False)
    # Used to find DOS based upon start times
    dos_datetime = forms.DateTimeField(
        widget=extrawidgets.SplitSelectDateTimeWidget(minute_step=15))
    # Used to find DOS based upon end times
    dos_endtime = forms.TimeField(
        widget=extrawidgets.SelectTimeWidget(minute_step=15))
    DURATION_CHOICES = (
        ('0', '0'),
        ('15', '15'),
        ('30', '30'),
        ('45', '45'),
        ('60', '60'),
        ('75', '75'),
        ('90', '90'),
        ('105', '105'),
        )
    REPEAT_CHOICES = (
        ('No', 'No'),
        ('One Day', 'One Day'),
        ('One Week', 'One Week'),
        ('Two Weeks', 'Two Weeks'),
        ('Three Weeks', 'Three Weeks'),
        ('Four Weeks', 'Four Weeks'),
        )
    dos_repeat = forms.ChoiceField(choices=REPEAT_CHOICES, required=False)
    dos_repeat_end_date = forms.DateField(required=False)

    def get_all_fields(self):
        """ Gets all the fields for this form. """
        return str(dir(self))


class DOSRecurr(db.Model):
    """ Model Class for all the recurring DOS. """
    userinfo = db.UserProperty()
    user_id = db.StringProperty()
    dos_base = db.ReferenceProperty(DOS)

    dos_recurr_datetime = db.DateTimeProperty()

    def get_hover_tip(self):
        """ Gets a blank hover tip for this DOS. """
        return ''

    def __unicode__(self):
        """ Returns a unicode string of DOS this DOSRecurr is based upon. """
        return self.dos_base.__unicode__()

    def get_blocked_time(self):
        """ Returns true if this DOSRecurr has a clientinfo set, False
            otherwise. """
        if not self.dos_base.clientinfo:
            return True
        return False

    def get_class_name(self):
        """ Returns an HTML class name based upon various attributes of this
            DOS. """
        if self.get_blocked_time():
            return 'blocked_time'
        return 'recurrClient'

    def get_background_color(self):
        """ Returns a background color based upon various attributes of this
            DOS. """
        if self.get_blocked_time():
            return 'blue'
        return 'yellow'

    def get_text_color(self):
        """ Returns a text color based upon various attributes of this
            DOS. """
        if self.get_blocked_time():
            return 'white'
        return 'blue'

    def get_calendar_absolute_url(self):
        if self.dos_recurr_datetime:
            return reverse('calendar_dos_recurr',
                           args=('%04d' % self.dos_recurr_datetime.year,
                                 '%02d' % self.dos_recurr_datetime.month,
                                 '%02d' % self.dos_recurr_datetime.day,
                                 '%02d' % self.dos_recurr_datetime.hour,
                                 '%02d' % self.dos_recurr_datetime.minute,
                                 '%d' % int(self.dos_base.get_id())))
        return self.dos_base.get_absolute_url()

    def get_id(self):
        return self.key().id_or_name()

    def get_starttime(self):
        return self.dos_recurr_datetime

    def get_endtime(self):
        return datetime.datetime.combine(self.dos_recurr_datetime.date(),
                                        self.dos_base.get_endtime().time())

    def get_note(self):
        if self.get_blocked_time():
            return self.dos_base.get_note()
        return ''

    def get_DOSForm(self, request, dos_datetime):
        form = DOSForm(request=request, initial={
            'clientinfo': self.dos_base.get_clientinfo_key(),
            'dos_datetime': dos_datetime,
            'dos_endtime': self.dos_base.get_endtime(),
            'session_type': self.dos_base.session_type,
            'dsm_code': self.dos_base.dsm_code,
            'type_pay': self.dos_base.type_pay,
            'amt_due': self.dos_base.amt_due,
            'dos_duration': self.dos_base.dos_duration,
            'dos_repeat_end_date': dos_datetime,
            })
        return form

    @staticmethod
    def safe_all(request=None, keys_only=False):
        return global_get_all(DOSRecurr, request=request, keys_only=keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        return global_get_by_id(DOSRecurr, ids, request=request, parent=None)


class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=200)


class Invoice(db.Model):
    clientinfo = db.ReferenceProperty(ClientInfo)
    userinfo = db.UserProperty()
    user_id = db.StringProperty()

    invoice_date = db.DateProperty(auto_now=True)
    start_date = db.DateProperty()
    end_date = db.DateProperty()

    def get_invoice_gen_date(self):
        return date_formatter(self.invoice_date)

    def get_start_date(self):
        return date_formatter(self.start_date)

    def get_end_date(self):
        return date_formatter(self.end_date)

    def __unicode__(self):
        return ''

    def get_all_dos_absolute_url(self):
        return ('/Mindwell/' + str(self.get_id()) + \
                '/all_dos/invoice_display/')

    def get_attended_only_absolute_url(self):
        return ('/Mindwell/' + str(self.get_id()) + \
                '/attended_only/invoice_display/')

    def get_all_dos_absolute_url_html(self):
        return ('/Mindwell/' + str(self.get_id()) + \
                '/all_dos/html/invoice_display/')

    def get_attended_only_absolute_url_html(self):
        return ('/Mindwell/' + str(self.get_id()) + \
                '/attended_only/html/invoice_display/')

    def get_absolute_url(self):
        return self.get_all_dos_absolute_url()

    def get_id(self):
        return self.key().id_or_name()

    @staticmethod
    def GetInvoice(request, receipt_dos):
        if receipt_dos is not None:
            print_receipt_dos = DOS.safe_get_by_id(int(receipt_dos), request)
            if print_receipt_dos:
                invoice = Invoice.safe_all(request).filter(
                        'start_date =',
                        print_receipt_dos.dos_datetime.date()
                    ).filter(
                        'end_date =',
                        print_receipt_dos.dos_datetime.date()
                    ).filter(
                       'clientinfo = ',
                       print_receipt_dos.clientinfo.key()
                   ).get()
                if not invoice:
                    invoice = Invoice(
                        clientinfo=print_receipt_dos.clientinfo,
                        user_id=pull_current_user_id_from_request(request),
                        start_date=print_receipt_dos.dos_datetime.date(),
                        end_date=print_receipt_dos.dos_datetime.date(),)
                    invoice.put()
                return invoice
        return None

    @staticmethod
    def safe_all(request=None, keys_only=False):
        return global_get_all(Invoice, request=request, keys_only=keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        return global_get_by_id(Invoice, ids, request=request, parent=None)


class InvoiceForm(forms.Form):
    this_year = datetime.date.today().year
    years = range(this_year - 5, this_year + 10)
    clientinfo = forms.ChoiceField(label='Client')
    start_date = forms.DateField(widget=SelectDateWidget(years=years))
    end_date = forms.DateField(widget=SelectDateWidget(years=years))
    user_id = db.StringProperty()

    def __init__(self, *args, **kwargs):

        self.base_fields['clientinfo'].choices = (
            ClientInfo.get_clientinfo_choices(kwargs.get('request')))
        if 'request' in kwargs:
            del kwargs['request']
        super(InvoiceForm, self).__init__(*args, **kwargs)


class DailyInvoiceForm(forms.Form):
    this_year = datetime.date.today().year
    years = range(this_year - 5, this_year + 10)
    start_invoice_date = forms.DateField(widget=SelectDateWidget(years=years))
    end_invoice_date = forms.DateField(widget=SelectDateWidget(years=years))


class InvoiceSettings(db.Model):
    userinfo = db.UserProperty()
    user_id = db.StringProperty()
    practice_name = db.StringProperty(multiline=True)
    header = db.StringProperty(multiline=True)
    right_header = db.StringProperty(multiline=True)
    footer = db.StringProperty(multiline=True)
    user_id = db.StringProperty()

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)

    @staticmethod
    def safe_all(request=None, keys_only=False):
        return global_get_all(InvoiceSettings, request, keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        return global_get_by_id(InvoiceSettings, ids, request=request,
                                parent=None)

    @staticmethod
    def Get(request=None):
        try:
            settings = InvoiceSettings.safe_all(request=request)[0]
            return settings
        except IndexError:
            return None

    def get_saved_url(self):
        return reverse('updated_invoice_settings', kwargs={'update': 'update'})


class InvoiceSettingsForm(forms.Form):
    practice_name = forms.CharField(max_length=500, widget=forms.Textarea,
                                    required=False)
    header = forms.CharField(max_length=500, widget=forms.Textarea,
                             required=False)
    right_header = forms.CharField(max_length=500, widget=forms.Textarea,
                                   required=False)
    footer = forms.CharField(max_length=500, widget=forms.Textarea,
                             required=False)

    def get_edit_template(self):
        return 'invoice_settings_template.html'

    @classmethod
    def get_default_form(cls):
        return cls()


class CustomFormSettings(db.Model):
    userinfo = db.UserProperty()
    user_id = db.StringProperty()
    reason_for_visit_choices = db.TextProperty()
    referrer_choices = db.TextProperty()
    session_type_choices = db.TextProperty()
    new_client_script = db.TextProperty()
    user_id = db.StringProperty()

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)

    @staticmethod
    def Get(request=None):
        return CustomFormSettings.GetSettings(request)

    @staticmethod
    def GetSettings(request=None):
        custom_form_settings = CustomFormSettings.safe_all(request=request)
        if custom_form_settings.count() > 0:
            return custom_form_settings[0]
        return CustomFormSettings()

    @staticmethod
    def safe_all(request=None, keys_only=False):
        return global_get_all(CustomFormSettings, request, keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        return global_get_by_id(CustomFormSettings, ids, request=request,
                                parent=None)

    def build_checkbox_list(self, attr):
        choices = []
        if getattr(self, attr):
            choices = getattr(self, attr).split('\n')
            choices = [choice for choice in choices if choice]
            choices = [Checkbox(choice.rstrip(), False)
                           for choice in choices]
        return choices

    def get_reason_for_visit_choices(self):
        return self.build_checkbox_list('reason_for_visit_choices')

    def get_referrer_choices(self):
        return self.build_checkbox_list('referrer_choices')

    def get_session_type_choices(self):
        return self.build_checkbox_list('session_type_choices')

    def get_new_client_script(self):
        new_client_script = ''
        if self.new_client_script:
            new_client_script = self.new_client_script.split('\n')
        return new_client_script

    def get_saved_url(self):
        return reverse('updated_custom_form_settings',
                       kwargs={'update': 'update'})


class CustomFormSettingsForm(forms.Form):
    reason_for_visit_choices = forms.CharField(widget=forms.Textarea(),
                                               required=False)
    referrer_choices = forms.CharField(widget=forms.Textarea(),
                                       required=False)
    session_type_choices = forms.CharField(widget=forms.Textarea(),
                                           required=False)
    new_client_script = forms.CharField(widget=forms.Textarea(),
                                        required=False)
    user_id = db.StringProperty()

    @classmethod
    def get_default_form(cls):
        return cls()

    def get_edit_template(self):
        return 'custom_form_settings_template.html'


class CalendarSettings(db.Model):
    userinfo = db.UserProperty()
    user_id = db.StringProperty()
    display_weekends = db.StringProperty()
    calendar_start_time = db.StringProperty()

    def update_model(self, values):
        for k, v in values.iteritems():
            setattr(self, k, v)

    @staticmethod
    def safe_all(request=None, keys_only=False):
        return global_get_all(CalendarSettings, request, keys_only)

    @staticmethod
    def safe_get_by_id(ids, request=None, parent=None):
        return global_get_by_id(CalendarSettings, ids, request=request,
                                parent=None)

    @staticmethod
    def GetCalendarSettings():
        try:
            return CalendarSettings.safe_all()[0]
        except IndexError:
            return None

    @staticmethod
    def Get(request=None):
        try:
            return CalendarSettings.safe_all()[0]
        except IndexError:
            return None

    @staticmethod
    def GetDisplayWeekend(calendar_settings):
        displayweekends = False
        if calendar_settings and calendar_settings.display_weekends == 'Yes':
            displayweekends = True
        return str(displayweekends).lower()

    @staticmethod
    def GetStartTime(calendar_settings):
        start_time = 6
        if calendar_settings:
            start_time = int(str(
                  calendar_settings.calendar_start_time).split(' ')[0])
            if 'pm' in calendar_settings.calendar_start_time:
                start_time += 12
            if start_time == 12 or start_time == 24:
                start_time -= 12
        return start_time

    def get_saved_url(self):
        return reverse('updated_calendar_settings',
                       kwargs={'update': 'update'})


class CalendarSettingsForm(forms.Form):
    DISPLAY_WEEKEND_CHOICES = (
        ('No', 'No'),
        ('Yes', 'Yes'),
    )
    display_weekends = forms.ChoiceField(
        label='Display Weekends by Default',
        choices=DISPLAY_WEEKEND_CHOICES)
    CALENDAR_START_TIME_CHOICES = (
      ('12 am', '12 am'),
      ('1 am', '1 am'),
      ('2 am', '2 am'),
      ('3 am', '3 am'),
      ('4 am', '4 am'),
      ('5 am', '5 am'),
      ('6 am', '6 am'),
      ('7 am', '7 am'),
      ('8 am', '8 am'),
      ('9 am', '9 am'),
      ('10 am', '10 am'),
      ('11 am', '11 am'),
      ('12 pm', '12 pm'),
      ('1 pm', '1 pm'),
      ('2 pm', '2 pm'),
      ('3 pm', '3 pm'),
      ('4 pm', '4 pm'),
      ('5 pm', '5 pm'),
      ('6 pm', '6 pm'),
      ('7 pm', '7 pm'),
      ('8 pm', '8 pm'),
      ('9 pm', '9 pm'),
      ('10 pm', '10 pm'),
      ('11 pm', '11 pm'),
    )
    calendar_start_time = forms.ChoiceField(
        choices=CALENDAR_START_TIME_CHOICES,
        label='Calendar Start Time')

    @classmethod
    def get_default_form(cls):
        return cls(initial={'display_weekends': 'No',
                            'calendar_start_time': '6 am'})

    def get_edit_template(self):
        return 'calendar_settings_template.html'


class UserInfoForm(forms.Form):

    user_email_address = forms.CharField(max_length=200)
