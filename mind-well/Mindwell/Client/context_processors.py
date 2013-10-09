from google.appengine.api import users
from google.appengine.ext import db
from Mindwell.Client import models
import view_common


def get_current_user(request):
    current_user = None
    if 'current_user' in request.COOKIES:
        if str(request.COOKIES['current_user']) != 'Self':
            try:
                current_user = models.UserPermission().safe_get(
                    request.COOKIES['current_user'])
            except db.BadKeyError:
                view_common.log_access_violation('get_current_user')
    return {'current_user': current_user}


def get_logout_url(request):
    return {"logout_url": users.create_logout_url('/')}


def get_permitted_users(request):
    # explicitly looking up just this users info, so request=None
    permitted_users = models.UserPermission().safe_all(request=None).filter(
        'user_approved = ', 'Approved')
    return {"permitted_users": permitted_users}
