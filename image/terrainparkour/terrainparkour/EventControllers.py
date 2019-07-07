import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from terrainparkour.serializers import *
from terrainparkour.allmodels import *

from terrainparkour.RaceEventHelpers import *

from terrainparkour.ActionResult import ActionResult
from terrainparkour import PlaceHelpers
from terrainparkour import util


def getUpcomingEvents(request):
    now=utcnow()
    events=RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now)
    resp={'success':True, 'res':[jsonEvent(e) for e in events]}
    return JsonResponse(resp)

def getEphemeralEventsEndpoint(request):
    now=utcnow()
    #for now this only returns quickraces - other events should be discovered.
    events=getEphemeralEvents()
    if events:
        evlist = [jsonEvent(e) for e in events]
    else:
        evlist = []
    resp={'success':True, 'res':evlist}
    return JsonResponse(resp)

def getCurrentEventsEndpoint(request):
    now=utcnow()
    #for now this only returns quickraces - other events should be discovered.
    events=getCurrentEvents()
    if events:
        evlist = [jsonEvent(e) for e in events]
    else:
        evlist = []
    resp={'success':True, 'res':evlist}
    return JsonResponse(resp)
