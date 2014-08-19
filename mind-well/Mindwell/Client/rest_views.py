import json

from django.http import HttpResponse
from google.appengine.ext import db

import common
import models


def rest_dos(request):
    dos = models.DOS.safe_all(request=request).fetch(
        common.get_maximum_num_dos_fetch())
    return HttpResponse(json.dumps([d.get_rest() for d in dos]), content_type="application/json")
