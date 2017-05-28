import datetime, math, os

from django.http import JsonResponse
from django.http import HttpResponse
from terrainapp.models import *
import admin

def getSecretKey():
    res=open('secret.txt','r').read().strip()
    return res

secret=getSecretKey()
noKey={'error':True,'message':'missing secret key'}

#there is a required secret key
def security(func, should_log_user_source=False, first=False):
    def inner(request, *kwgs):
        provided_secret=request.GET.get('secret')
        exi=RequestSource.objects.filter(ip=request.META['REMOTE_ADDR'])
        if exi.count()>0:
            source=exi[0]
        else:
            source=RequestSource(ip=request.META['REMOTE_ADDR'])
            source.save()
        if provided_secret!=secret:
            failure=FailedSecurityAttempt(source=source, params=request.META['QUERY_STRING'])
            failure.save()
            source.failure_count=source.failure_count+1
            source.save()
            return JsonResponse(noKey)
        if should_log_user_source:
            logUser(kwgs[0], source, first)
        source.success_count=source.success_count+1
        source.save()
        return func(request, *kwgs)
    return inner

def test(request):
    return JsonResponse({"result":True, "message":'test.'})

def logUser(userId, source, first):
    '''log this user coming from this source.'''
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    userSource, created=UserSource.objects.get_or_create(user=user, source=source, first=first)
    userSource.count=userSource.count+1
    userSource.save()

def robloxUserJoined(request, userId, username):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    if user.username!=username:
        user.username=username
        user.save()
    res={'success':True}
    join=GameJoin(user=user)
    join.save()
    return JsonResponse(res)

def robloxUserLeft(request, userId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    leave=GameLeave(user=user)
    leave.save()
    return JsonResponse({'success':True})

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

def userFoundSign(request, userId, signId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    sign=tryGet(Sign, {'signId':signId})
    if not sign:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(signId)})
    find=Find.objects.filter(user=user, sign=sign)
    if find.count()==0:
        find, created=Find.objects.get_or_create(user=user, sign=sign)
    return JsonResponse({'success':True, 'created':created, 'signTotalFindCount':sign.finds.count(),'userFindCount':user.finds.count()})

def tryGet(cls, params):
    res=cls.objects.filter(**params)
    if res.count()>0:
        return res[0]
    return None

def setSignPosition(request, signId, name, x,y,z):
    sign=tryGet(Sign, {'signId':signId})
    if not sign:
        sign=Sign(signId=signId, name=name, x=x, y=y, z=z)
        sign.save()
        #return JsonResponse({'error':True,'message':'no such sign %s'%str(signId)})
    sign.x=x
    sign.y=y
    sign.z=y
    sign.name=name
    sign.save()
    return JsonResponse({'success':True})

def userFinishedRun(request, userId, startId, endId, raceMilliseconds):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=tryGet(Sign, {'signId':startId})
    if not start:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(startId)})
    end=tryGet(Sign, {'signId':endId})
    if not end:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(endId)})
    race, created=Race.objects.get_or_create(start=start, end=end)
    raceMilliseconds=math.ceil(int(raceMilliseconds))
    exi=Run.objects.filter(user=user, race=race, raceMilliseconds=raceMilliseconds)
    if exi.count()>0:
        #run with this exact time, user, race already exists, no duplicates allowed!
        return JsonResponse({'success':True })
    run=Run(user=user, race=race, raceMilliseconds=raceMilliseconds)
    run.save()
    resp={'success':True}
    resp=maybeCreateBestrun(user, run, resp)
    if 'place' in resp and resp['place']:
        run.place=resp['place']
        run.save()
    return JsonResponse(resp)

def maybeCreateBestrun(user, run, resp):
    exi=BestRun.objects.filter(user__userId=user.userId, race__id=run.race.id)
    placesNeedAdjustment=False
    if exi.count()>0:
        bestrun=exi[0]
        if bestrun.raceMilliseconds>run.raceMilliseconds:
            bestrun.raceMilliseconds=run.raceMilliseconds
            bestrun.save()
            placesNeedAdjustment=True
    else:
        bestrun=BestRun(user=user, raceMilliseconds=run.raceMilliseconds, race=run.race)
        bestrun.save()
        placesNeedAdjustment=True
    if placesNeedAdjustment:
        adjustPlaces(user, run, bestrun)
    bestrun=BestRun.objects.get(id=bestrun.id)
    #if we placed in the top ten, then return topTenCount and wrCount for those record checking on client.
    resp['place']=bestrun.place
    if bestrun.place<=10:
        resp['topTenCount']=user.bestruns.exclude(place=None).count()
    if bestrun.place==1:
        resp['wrCount']=user.bestruns.filter(place=1).count()
    return resp

def adjustPlaces(user, run, bestrun):
    #we know bestrun is in the top 10.
    res=getTopTen(run.race.start.signId, run.race.end.signId, extra=True)
    ii=1
    for bestrun in res:
        useii=ii<=10 and ii or None
        if bestrun.place!=useii:
            bestrun.place=useii
            bestrun.save()
        ii=ii+1

def getTotalWorldRecordCountByUser(request, userId):
    bests=BestRun.objects.filter(user__userId=userId).filter(place=1)
    return JsonResponse({'count':bests.count()})

def getTotalTopTenCountByUser(request, userId):
    topTens=BestRun.objects.filter(user__userId=userId).exclude(place=None)
    return JsonResponse({'count':topTens.count()})

def getRaceInfoByUser(request, userId, startId, endId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=tryGet(Sign, {'signId':startId})
    if not start:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(startId)})
    end=tryGet(Sign, {'signId':endId})
    if not end:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(endId)})
    race=tryGet(Race, {start:start, end:end})
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
    res=getTopTen(startId, endId)
    res=[jsonRun(r) for r in res]
    return JsonResponse({'res':res})

def getTopTen(startId, endId, extra=False):
    lim=10
    if extra:
        lim=11
    res=BestRun.objects.filter(race__start__signId=startId, race__end__signId=endId).order_by('raceMilliseconds')[:lim]
    return res

def jsonRun(r):
    res={'raceMilliseconds':r.raceMilliseconds,
        'username':r.user.username,
        'userId':r.user.userId,
        'place':r.place}
    return res
