import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from terrainparkour.allmodels import *
from terrainparkour import admin

from terrainparkour.webutil import security, postSecurity, logUser

def getListByType(request, source):
    resp={'success':False}
    listType=request.POST.get('topType')
    if not listType:
        return JsonResponse(resp)
    days=request.POST.get('days') or 1
    days=int(days)
    if listType=='wrsToday': #most WRs of any user
        return getWrsDays(days)
    else:
        import ipdb;ipdb.set_trace()

def getWrsDays(days):
    #BestRun.objects.exclude(place=None).filter(updated__gt=today)
    lim=10
    raw='select group_concat(br.id) as gc, ru.id, ru.username as username, ru.userId as userId, count(*) as ct from bestrun br inner join robloxuser ru on ru.id=br.user_id where br.updated>subdate(curdate(),%d) and place is not null group by 2,3,4 order by 5 desc limit %d'%(days, lim)
    dat=BestRun.objects.raw(raw)
    res=[]
    for el in dat:
        res.append(jsonWr(el))
    return JsonResponse({'data':res})

def jsonWr(el):
    return {'username':el.username,
        'count':el.ct,
        'userId':el.userId
        }
