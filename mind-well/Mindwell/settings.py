import os

DEBUG = True
TEMPLATE_DEBUG = True

ROOT_URLCONF = 'Mindwell.urls'

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''


MIDDLEWARE_CLASSES = (
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'django.middleware.common.CommonMiddleware',
    'Mindwell.Client.middleware.AuthorizedUserMiddleware'
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'Mindwell.Client.context_processors.get_current_user',
    'Mindwell.Client.context_processors.get_logout_url',
    'Mindwell.Client.context_processors.get_permitted_users'
)
INSTALLED_APPS = (
    'Mindwell.Client',
)


ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT_PATH + '/templates',
)
