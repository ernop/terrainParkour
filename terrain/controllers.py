import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from allmodels import *

from ActionResult import ActionResult
import PlaceHelpers
import util

def test(request):
    return JsonResponse({"result":True, "message":'test.'})

def robloxUserJoined(request, userId, username):
    robloxuser, created=RobloxUser.objects.get_or_create(userId=userId)
    if robloxuser.username!=username:
        robloxuser.username=username
        robloxuser.save()
    res={'success':True}
    actionResult = TixTransaction.checkUserJoined(robloxuser)
    res['ActionResults']=[]
    if actionResult:
        res['ActionResults'].append(vars(actionResult))
    join=GameJoin(user=robloxuser)
    join.save()
    return JsonResponse(res)

def robloxUserLeft(request, userId):
    userId=int(userId)
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    GameJoin.playerLeft(userId, utcnow())
    return MyJsonResponse({'success':True})

def robloxUserDied(request, userId, x, y, z):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    res={'success':True}
    join=UserDied(user=user, x=x, y=y, z=z)
    join.save()
    return JsonResponse(res)

def robloxUserQuit(request, userId, x, y, z):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    res={'success':True}
    join=UserQuit(user=user, x=x, y=y, z=z)
    join.save()
    return JsonResponse(res)

def robloxUserReset(request, userId, x, y, z):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    res={'success':True}
    join=UserReset(user=user, x=x, y=y, z=z)
    join.save()
    return JsonResponse(res)

def setUserBanLevel(request, userId, banLevel):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    if banLevel!=user.banLevel:
        user.banLevel=banLevel
        user.save()
        return JsonResponse({'success':True})
    return JsonResponse({'success':True, 'message':'no change'})

def getUserBanLevel(request, userId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    return JsonResponse({'banLevel':user.banLevel})

def setSignPosition(request, signId, name, x,y,z):
    sign=util.tryGet(Sign, {'signId':signId})
    if not sign:
        sign=Sign(signId=signId, name=name, x=x, y=y, z=z)
        sign.save()
    sign.x=x
    sign.y=y
    sign.z=z
    sign.name=name
    sign.save()
    return JsonResponse({'success':True})

def getTotalWorldRecordCountByUser(request, userId):
    bests=BestRun.objects.filter(user__userId=userId).filter(place=1)
    return JsonResponse({'count':bests.count()})

def getTotalTopTenCountByUser(request, userId):
    topTens=BestRun.objects.filter(user__userId=userId).exclude(place=None)
    return JsonResponse({'count':topTens.count()})

def getRaceInfoByUser(request, userId, startId, endId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=util.tryGet(Sign, {'signId':startId})
    if not start:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(startId)})
    end=util.tryGet(Sign, {'signId':endId})
    if not end:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(endId)})
    race=util.tryGet(Race, {start:start, end:end})
    runs=Run.objects.filter(start=start, end=end, user=user)
    bests=getBestTimesByRace(request, startId, endId)
    res={'runs':runs.count(),}
    return JsonResponse(res)

def getUserSignFinds(request, userId):
    res=Find.objects.filter(user__userId=userId)
    res={f.sign.signId:True for f in res}
    return JsonResponse(res)

def getTotalFindCountBySign(request, signId):
    res=Find.objects.filter(sign__signId=signId)
    return JsonResponse({'count':res.count()})

def getTotalFindCountByUser(request, userId):
    res=Find.objects.filter(user__userId=userId)
    return JsonResponse({'count':res.count()})

def getTotalRunCount(request):
    return JsonResponse({'count':Run.objects.count()})

def getTotalRaceCount(request):
    return JsonResponse({'count':Race.objects.count()})

def getStatsByUser(request, userId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    res={'finds':Find.objects.filter(user__userId=userId).count(),
         'races':BestRun.objects.filter(user__userId=userId).count(),
         'distinctRuns': Run.objects.filter(user__userId=userId).count(),
         'toptens':BestRun.objects.filter(user__userId=userId).exclude(place=None).count(),
         'wrs':BestRun.objects.filter(user__userId=userId).filter(place=1).count(),
         'tix':TixTransaction.GetTixBalanceByUser(user),
         #'tixNow':TixTransaction.GetTixBalanceByUser(user),
         }
    return JsonResponse(res)

def getTotalRaceCountByDay(request):
    today=datetime.datetime.today()-datetime.timedelta(days=1)
    tomorrow=datetime.datetime.today()
    races=Race.objects.filter(created__gte=today, created__lt=tomorrow)
    return JsonResponse({'count':races.count()})

def getTotalRunCountByDay(request):
    today=datetime.datetime.today()-datetime.timedelta(days=1)
    tomorrow=datetime.datetime.today()
    res=Run.objects.filter(created__gte=today, created__lt=tomorrow)
    return JsonResponse({'count':res.count()})

def getTotalRunCountByUserAndDay(request, userId):
    today=datetime.datetime.today()-datetime.timedelta(days=1)
    tomorrow=datetime.datetime.today()
    res=Run.objects.filter(created__gte=today, created__lt=tomorrow, user__userId=userId)
    return JsonResponse({'count':res.count()})

def getTotalFindCountByDay(request):
    today=datetime.datetime.today()-datetime.timedelta(days=1)
    tomorrow=datetime.datetime.today()
    res=Find.objects.filter(created__gte=today, created__lt=tomorrow)
    return JsonResponse({'count':res.count()})

def getTotalRunCountByUserAndRace(request, userId, startId, endId):
    res=Run.objects.filter(race__start__signId=startId, race__end__signId=endId, user__userId=userId)
    return JsonResponse({'count':res.count()})

def getTotalRunCountByRace(request, startId, endId):
    res=Run.objects.filter(race__start__signId=startId, race__end__signId=endId)
    return JsonResponse({'count':res.count()})

def getTotalBestRunCountByRace(request, startId, endId):
    res=BestRun.objects.filter(race__start__signId=startId, race__end__signId=endId)
    return JsonResponse({'count':res.count()})

def getTotalRunCountByUser(request, userId):
    res=Run.objects.filter(user__userId=userId)
    return JsonResponse({'count':res.count()})

def getTotalRaceCountByUser(request, userId):
    res=BestRun.objects.filter(user__userId=userId)
    return JsonResponse({'count':res.count()})

def getBestTimesByRace(request, startId, endId):
    start=Sign.objects.get(signId=startId)
    end=Sign.objects.get(signId=endId)
    race,created=Race.objects.get_or_create(start=start, end=end)
    res=PlaceHelpers.getTopTen(race)
    res=[jsonRun(r) for r in res]
    return JsonResponse({'res':res})


def userSentMessage(request, source):
    resp={'success':True}
    userId=request.POST.get('userId') or None
    if not userId: return resp
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    rawtext=request.POST.get('rawtext') or ''
    filteredtext=request.POST.get('filteredtext') or ''
    mm=ChatMessage(user=user, requestsource=source, rawtext=rawtext, filteredtext=filteredtext)
    mm.save()
    return JsonResponse(resp)

def receiveError(request, source):
    code=request.POST.get('code') or ''
    data=request.POST.get('data') or ''
    message=request.POST.get('message') or ''
    err=GameServerError(requestsource=source, code=code, message=message, data=data)
    err.save()
    resp={'success':True}
    return JsonResponse(resp)

def getTixBalanceByUsername(request, username):
    robloxuser=RobloxUser.objects.filter(username=username)
    if not robloxuser:
        resp={'success':False, 'message':"Failed to get tix balance. No such user."}
        return JsonResponse(resp)
    balance=TixTransaction.GetTixBalanceByUser(robloxuser[0])
    resp={'success':True,
          'balance':balance,
          'message':"Balance for %s: %d tix"%(username, balance)}
    return JsonResponse(resp)

#def postEndpoint(request, data):
#    method=request.POST.get('method')
#    if method=='userFinishedRun':
#        userId=request.POST.get('userId')
#        playerIds=request.POST.get('playerIds')
#        startId=request.POST.get('startId')
#        endId=request.POST.get('endId')
#        raceMilliseconds=request.POST.get('raceMilliseconds')
#        return userFinishedRun(userId=userId, playerIds=playerIds, endId=endId, startId=startId,raceMilliseconds=raceMilliseconds)
    