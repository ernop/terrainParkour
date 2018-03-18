import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from allmodels import *

from webutil import security, postSecurity, logUser
from ActionResult import ActionResult
from TixTransactionAmountEnum import *
from TixTransactionTypeEnum import *

import util

def test(request):
    return JsonResponse({"result":True, "message":'test.'})

#return all that initial stuff with fewer requests!
def getUserInitialBlob(request, userId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    res={}
    #extend this to other stuff later?
    res['banLevel']=user.banLevel
    return JsonResponse(res)

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

def userFoundSign(request, userId, signId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    actionResults=[]
    sign=tryGet(Sign, {'signId':signId})
    if not sign:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(signId)})
    find=Find.objects.filter(user=user, sign=sign)
    foundNew = False #we need this to update client side cache, and check badges over there.
    if find.count()==0:
        find, foundNew=Find.objects.get_or_create(user=user, sign=sign)

    #create an actionresult.
    signFindCount = Find.objects.filter(sign=sign).count()
    userFindCount=Find.objects.filter(user=user).count()
    totalSignCount=Sign.objects.count()
    resp={}
    if foundNew:
        reason = TixTransactionTypeEnum.NEW_FIND
        amount = TixTransactionAmountEnum[reason.name].value
        tt = TixTransaction(user=user, amount=amount, transactionday=None, reason=reason.value)
        tt.save()

        if signFindCount==1:
            message = "You discovered %s!"%(sign.name)
        else:
            message = "You were the %s person to find %s!"%(util.getCardinal(signFindCount), sign.name)
    
        message="%s\nYou've found %d out of %d!\nAnd this earned you %d tix!"%(message, userFindCount, totalSignCount, amount)
        ar=ActionResult(notify=True, userId=userId, message=message)

        resp={'success':True, 'foundNew':foundNew, 'created':foundNew, 'userFindCount':user.finds.count()}
    
        actionResults.append(vars(ar))
        otherMessage ="%s found %s! They've found %d total."%(user.username, sign.name, userFindCount)
        #would be nice to have customized messages to every other player about the actions of someone!
        ar=ActionResult(notify=True, userId=userId, message=otherMessage, notifyAllExcept=True)
        actionResults.append(vars(ar))

    resp['ActionResults']=actionResults
    return JsonResponse(resp)

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
    sign.x=x
    sign.y=y
    sign.z=z
    sign.name=name
    sign.save()
    return JsonResponse({'success':True})

def makeArForCreatedRace(user, race):
    reason = TixTransactionTypeEnum.NEW_RACE
    amount = TixTransactionAmountEnum[reason.name].value
    tt = TixTransaction(user=user, amount=amount, transactionday=None, reason=reason.value)
    tt.save()
    message='You have earned %d tix for discovering a new run!'%amount
    ar=ActionResult(notify=True, userId=user.userId, message=message)
        
    return vars(ar)

def makeArsForImprovedPlace(user, race):
    res=[]
    reason = TixTransactionTypeEnum.NEW_WR
    amount = TixTransactionAmountEnum[reason.name].value
    tt = TixTransaction(user=user, amount=amount, transactionday=None, reason=reason.value)
    tt.save()
        
    message='You have earned %d tix for getting a new WR!'%amount
    ar=ActionResult(notify=True, userId=user.userId, message=message)
    res.append(vars(ar))
        
    message='%s earned %d tix for getting a new WR on race %s!'%(user.username, amount, race)
    ar=ActionResult(notify=True, userId=user.userId, message=message, notifyAllExcept=True)
    res.append(vars(ar))
    return res


def maybeCreateBestRun(user, run):
    resp={}
    exi=BestRun.objects.filter(user__userId=user.userId, race__id=run.race.id)
    placesNeedAdjustment=False
    thisPlace=None
    if exi.count()>0: #there should not really ever be 2+ of these.
        bestrun=exi[0]
        if bestrun.raceMilliseconds>run.raceMilliseconds:
            bestrun.raceMilliseconds=run.raceMilliseconds
            bestrun.save()
            placesNeedAdjustment=True
        thisPlace=bestrun.place
    else:
        bestrun=BestRun(user=user, raceMilliseconds=run.raceMilliseconds, race=run.race)
        bestrun.save()
        placesNeedAdjustment=True
    oldPlace = bestrun.place
    if placesNeedAdjustment:
        thisPlace=adjustPlaces(user, run)
    
    bestrun = BestRun.objects.get(id=bestrun.id)
    #if we placed in the top ten, then return topTenCount and wrCount for those record checking on client.
    
    resp['place']=thisPlace
    resp['improvedPlace']=oldPlace is None or bestrun.place<oldPlace
    if bestrun.place:
        if bestrun.place<=10:
            resp['userTotalTopTenCount']=user.bestruns.exclude(place=None).count()
        if bestrun.place==1:
            resp['userTotalWRCount']=user.bestruns.filter(place=1).count()
    return resp

def adjustPlaces(user, run):
    #we know bestrun is in the top 10.
    res=getTopTen(run.race, extra=True)
    ii=1
    thisPlace=None
    for bestrun in res:
        useii = ii <= 10 and ii or None
        if bestrun.place != useii:
            bestrun.place = useii
            bestrun.save()
            if thisPlace==None and bestrun.raceMilliseconds==run.raceMilliseconds:
                thisPlace=useii
        ii=ii+1
    return thisPlace


def userFinishedRun(userId, startId, endId, raceMilliseconds, playerIds):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=tryGet(Sign, {'signId':startId})
    if not start:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(startId)})
    end=tryGet(Sign, {'signId':endId})
    if not end:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(endId)})
    race, createdRace=Race.objects.get_or_create(start=start, end=end)
    actionResults=[]
    if createdRace:
        actionResults.append(makeArForCreatedRace(user, race))

    raceMilliseconds=math.ceil(int(raceMilliseconds))
    run=Run(user=user, race=race, raceMilliseconds=raceMilliseconds)
    run.save()
    #import ipdb;ipdb.set_trace()
    resp=maybeCreateBestRun(user, run)
    if 'place' in resp and resp['place']:
        #add place onto the run too, for convenience
        run.place=resp['place']
        run.save()
    if resp['place']==1 and resp['improvedPlace']: #bit annoying that they can farm tix by gradually improving WR time.
        #grant new tixtransaction.
        actionResults.extend(makeArsForImprovedPlace(user, race))

    
    #if resp['improvedPlace']:
    otherPlayerIds = set([int(p) for p in playerIds.split(',') if int(p)!=userId])

    #always notify if you push these guys down.
    otherPlayerIds.add(90115385) #brou
    otherPlayerIds.add(164062733) #verv

    if int(userId) in otherPlayerIds:
        otherPlayerIds.remove(int(userId))
    
    top10=getTopTen(race, extra=True)
    ars=makeRelativeActionResult(user, resp, top10, otherPlayerIds, race)
    if ars:
        actionResults.extend(ars)
    #see if anybody else in the server was in the list!
    #if they were higher, say "x tried to beat your record"
    #if they were lower and bumped, say "x bumped you down!/x beat your record"

    resp['ActionResults']=actionResults
    return JsonResponse(resp)

def makeRelativeActionResult(user, resp, top10, otherPlayerIds, race):
    myPlace=resp['place']
    ars=[]
    if myPlace==None or myPlace>=11:
        return ars
    if not resp['improvedPlace']:
        return ars

    for br in top10:
        if br.user.userId in otherPlayerIds:
            mymessage,othermessage=getMessage(br, user, myPlace, race)
            if mymessage:
                ar=ActionResult(notify=True, userId=user.userId, message=mymessage)
                ars.append(vars(ar))
            if othermessage:
                ar=ActionResult(notify=True, userId=br.user.userId, message=othermessage)
                ars.append(vars(ar))
    return ars

def getMessage(br, user, myPlace, race):
    mymessage=''
    othermessage=''
    if br.place==None: #knocked them out.
        mymessage="You knocked %s out of the top 10!"%(br.user.username)
        othermessage="%s knocked you out of the top 10 in the race %s"%(user.username, race)
    elif br.place<myPlace: #they are still winning
        mymessage='%s holds %s place in this race!'%(br.user.username, util.getCardinal(br.place))
        othermessage='%s is approaching your place %s in the race %s!! (they are %s)'%\
            (user.username, util.getCardinal(br.place), race, util.getCardinal(myPlace))
    elif br.place>myPlace: #pushed them down.
        mymessage='You pushed %s down to %s place!'%(br.user.username, util.getCardinal(br.place))
        othermessage='%s pushed you down to %s place in the race %s! They are %s.'%(user.username, util.getCardinal(br.place), race, util.getCardinal(myPlace))
    return mymessage, othermessage
    
    
    #if otherplayer is in the top 10, figure out the state.


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
    start=Sign.objects.get(signId=startId)
    end=Sign.objects.get(signId=endId)
    race,created=Race.objects.get_or_create(start=start, end=end)
    res=getTopTen(race)
    res=[jsonRun(r) for r in res]
    return JsonResponse({'res':res})


#what rules should we use to get a power for a user?
# what kind of powers are there?
# speed up
# superspeed, no jumps
# normal speed, super jump
#
def getPowerForUser(userId):
    pasPowers=Power.object.filter(user=user)
    return Power.objects.get(1)

def getTopTen(race, extra=False):
    lim=10
    if extra:
        lim=11
    res=BestRun.objects.filter(race=race).order_by('raceMilliseconds')[:lim]
    return res

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

def getUpcomingEvents(request):
    now=utcnow()
    events=RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now)
    resp={'success':True, 'res':[jsonEvent(e) for e in events]}
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

def postEndpoint(request, data):
    method=request.POST.get('method')
    if method=='userFinishedRun':
        userId=request.POST.get('userId')
        playerIds=request.POST.get('playerIds')
        startId=request.POST.get('startId')
        endId=request.POST.get('endId')
        raceMilliseconds=request.POST.get('raceMilliseconds')
        return userFinishedRun(userId=userId, playerIds=playerIds, endId=endId, startId=startId,raceMilliseconds=raceMilliseconds)
    