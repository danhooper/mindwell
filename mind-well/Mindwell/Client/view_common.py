import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from google.appengine.api import users
from google.appengine.ext import db
from Mindwell.Client import models
from django.utils.html import escape


def save_entity(request, entity):
#    entity.userinfo = models.pull_current_user_from_request(request)
    entity.user_id = models.pull_current_user_id_from_request(request)
    #entity.userinfo.user_id()
    entity.put()
    return entity




def log_access_violation(function):
    current_user = users.get_current_user()
    if current_user:
        logging.error('Access Violation: %s user: %s' % (
            function,
            current_user.email()))
    else:
        logging.error('Access Violation: %s no user logged in' % (
            function))


def CheckUserNotAllowed():
    if not models.UserInfo.CurrentUserAllowed():
        return HttpResponseRedirect('/Mindwell/UserNotAllowed')
    return False


def prefetch_refprops(entities, *props):
    if not entities:
        return
    non_empty_entities = [entity for entity in entities
                          for prop in props
                          if prop.get_value_for_datastore(entity)]
    fields = [(entity, prop) for entity in non_empty_entities
              for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]

    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)) if x)
    for (entity, prop), ref_key in zip(fields, ref_keys):
        try:
            if ref_entities[ref_key]:
                prop.__set__(entity, ref_entities[ref_key])
        except KeyError:
            logging.exception('Error getting reference key for %s' % str(ref_key))


def greetings(request):
    if 'current_user' in request.COOKIES:
        response = HttpResponseRedirect('/Mindwell/show_client/')
        response.delete_cookie('current_user')
    else:
        response = HttpResponseRedirect('/Mindwell/show_client/')

    return response


def usernotallowed(request):
    return render_to_response("usernotallowed_template.html", {
        "logout_url": users.create_logout_url('/'),
    })


def add_popup(render_to_response_dict, popup):
    if 'popups' in render_to_response_dict:
        render_to_response_dict['popups'].append(popup)
    else:
        render_to_response_dict['popups'] = [popup]


def escape_json(text):
    """
    escape html using django (replace single slash with double for javascript
    and finally put back in our <br/>
    """
    return escape(text).replace('\\', '\\\\'
        ).replace('&lt;br/&gt;', '<br/>'
        ).expandtabs(1)


def prevent_acting_as(func):
    ''' Prevents other users from accessing the view.  Useful for protecting
        things like permission settings for users.
    '''
    def decorator(*args, **kwargs):
        request = args[0]
        if (users.get_current_user().user_id() !=
            models.pull_current_user_id_from_request(request)):
            logging.warning('Access violation %s' % str(func))
            return HttpResponseRedirect('/Mindwell/show_client/')
        else:
            return func(*args, **kwargs)
    return decorator
