import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from allmodels import *

from RaceEventHelpers import *

from ActionResult import ActionResult
import PlaceHelpers
import util


def getUpcomingEvents(request):
    now=utcnow()
    events=RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now)
    resp={'success':True, 'res':[jsonEvent(e) for e in events]}
    return JsonResponse(resp)

def getCurrentEvents(request):
    now=utcnow()
    events=GetActiveRaceEvents()
    resp={'success':True, 'res':[jsonEvent(e) for e in events]}
    return JsonResponse(resp)
