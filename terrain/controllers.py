from django.http import JsonResponse
from terrainapp.models import *
import admin

def getSecretKey():
    res=open('secret.txt','r').read().strip()
    return res

secret=getSecretKey()
noKey={'error':True,'message':'missing secret key'}

#there is a required secret key
def security(func):
    def inner(request, *kwgs):
        provided_secret=request.GET.get('secret')
        if provided_secret!=secret:
            return JsonResponse(noKey)
        return func(request, *kwgs)
    return inner

def test(request):
    return JsonResponse({"result":True, "message":'test.'})

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
    return JsonResponse(res)

def userFoundSign(request, userId, signId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    sign=Sign.mustGet(signId=signId)
    if not sign:
        return {'error':True,'message':'no such sign %s'%str(signId)}
    find, created=UserFoundSign.objects.get_or_create(user=user, sign=sign)
    return JsonResponse({'success':'true', 'created':created, 'findCount':user.finds.Count()})

def userFinishedRace(request ,userId, startId, endId, raceMilliseconds):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=Sign.mustGet(Sign, signId=startId)
    if not start:
        return {'error':True,'message':'no such sign %s'%str(startId)}
    end=Sign.mustGet(Sign, signId=endId)
    if not end:
        return {'error':True,'message':'no such sign %s'%str(endId)}
    race, created=Race.objects.get_or_create(start=start, end=end)
    race.save()
    run=Run(user=user, race=race, raceMilliseconds=raceMilliseconds)
    run.save()
    return JsonResponse({'success':'true'})

def getUserSignFinds(request, userId):
    res=Find.objects.where(user__userId=userId)
    res={f.signId:True for f in res}
    return JsonResponse(res)

def getTotalFindCountBySign(request, signId):
    res=Find.objects.where(sign__id=signId)
    return JsonResponse({'count':res.Count()})

def getTotalFindCountByUser(request, userId, signId):
    res=Run.objects.where(start__id=startId, end__id=endId)
    return JsonResponse({'count':res.Count()})

def getTotalRunCountByDay(request):
    today=datetime.datetime.today()
    tomorrow=datetime.datetime.today()+datetime.timedelta(days=1)
    res=Run.objects.where(created__gte=today, created__lt=tomorrow)
    return JsonResponse({'count':res.Count()})

def getTotalRunCountByUserAndDay(request, userId):
    today=datetime.datetime.today()
    tomorrow=datetime.datetime.today()+datetime.timedelta(days=1)
    res=Run.objects.where(created__gte=today, created__lt=tomorrow, user__userId=userId)
    return JsonResponse({'count':res.Count()})

def getTotalFindCountByDay(request):
    today=datetime.datetime.today()
    tomorrow=datetime.datetime.today()+datetime.timedelta(days=1)
    res=Find.objects.where(created__gte=today, created__lt=tomorrow)
    return JsonResponse({'count':res.Count()})

def getTotalRunCountByUserAndRace(request, userId, startId, endId):
    res=Run.objects.where(start__id=startId, end__id=endId, user__userId=userId)
    return JsonResponse({'count':res.Count()})

def getTotalRunCountByRace(request, startId, endId):
    res=Run.objects.where(start__id=startId, end__id=endId)
    return JsonResponse({'count':res.Count()})

def getTotalRunCountByUser(request, userId):
    res=Run.objects.where(user__userId=userId)
    return JsonResponse({'count':res.Count()})

def getBestTimesByRace(request, startId, endId):
    res=Run.objects.where(start__id=startId, end__id=endId).OrderBy(run__milliSeconds__asc)[:10]
    res=[jsonRun(r) for r in res]
    return JsonResponse({'count':res})

def jsonRun(r):
    res={'milliSeconds':r.milliSeconds,
        'username':r.user.username,
        'userId':r.user.userId}
    return res














