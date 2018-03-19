import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from allmodels import *
import PlaceHelpers

from ActionResult import ActionResult
from TixTransactionAmountEnum import *
from TixTransactionTypeEnum import *
import RaceEventHelpers 

import util

def userFoundSign(request, userId, signId):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    actionResults=[]
    sign=util.tryGet(Sign, {'signId':signId})
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
        tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=reason.value)
        tt.save()

        if signFindCount==1:
            message = "You discovered %s!"%(sign.name)
        else:
            message = "You were the %s person to find %s!"%(util.getCardinal(signFindCount), sign.name)

        message="%s\nYou've found %d out of %d!\nAnd this earned you %d TIX!"%(message, userFindCount, totalSignCount, amount)
        ar=ActionResult(notify=True, userId=userId, message=message)

        resp={'success':True, 'foundNew':foundNew, 'created':foundNew, 'userFindCount':user.finds.count()}

        actionResults.append(vars(ar))
        otherMessage ="%s found %s! They've found %d total."%(user.username, sign.name, userFindCount)
        #would be nice to have customized messages to every other player about the actions of someone!
        ar=ActionResult(notify=True, userId=userId, message=otherMessage, notifyAllExcept=True)
        actionResults.append(vars(ar))

    resp['ActionResults']=actionResults
    return JsonResponse(resp)

def makeArForCreatedRace(user, race):
    reason = TixTransactionTypeEnum.NEW_RACE
    amount = TixTransactionAmountEnum[reason.name].value
    tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=reason.value)
    tt.save()
    message='You have earned %d TIX for discovering a new run!'%amount
    ar=ActionResult(notify=True, userId=user.userId, message=message)

    return vars(ar)

def makeArsForImprovedPlace(user, race):
    res=[]
    reason = TixTransactionTypeEnum.NEW_WR
    amount = TixTransactionAmountEnum[reason.name].value
    tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=reason.value)
    tt.save()

    message='You have earned %d TIX for getting a new WR!'%amount
    ar=ActionResult(notify=True, userId=user.userId, message=message)
    res.append(vars(ar))

    message='%s earned %d TIX for getting a new WR on race %s!'%(user.username, amount, race)
    ar=ActionResult(notify=True, userId=user.userId, message=message, notifyAllExcept=True)
    res.append(vars(ar))
    return res

def maybeCreateBestRun(user, run):
    resp={}
    placesNeedAdjustment=False
    exi=BestRun.objects.filter(user__userId=user.userId, race__id=run.race.id)
    if exi.count()>0: #there should not really ever be 2+ of these.
        bestRun=exi[0]
        if bestRun.raceMilliseconds>run.raceMilliseconds:
            bestRun.raceMilliseconds=run.raceMilliseconds
            bestRun.save()
            placesNeedAdjustment=True
        thisPlace = bestRun.place
        oldPlace = bestRun.place
    else:
        bestRun=BestRun(user=user, raceMilliseconds=run.raceMilliseconds, race=run.race)
        bestRun.save()
        placesNeedAdjustment=True
        thisPlace=None
        oldPlace=None
    if placesNeedAdjustment:
        bestRun=adjustPlaces(user, run.race)
        assert(user.id==bestRun.user.id)
        thisPlace=bestRun.place
    #if we placed in the top ten, then return topTenCount and wrCount for those record checking on client.

    resp['place']=thisPlace
    resp['improvedPlace']=False
    if oldPlace is None:
        if thisPlace is not None:
            resp['improvedPlace']=True

    elif bestRun.place and oldPlace > bestRun.place:
        resp['improvedPlace']=True

    if bestRun.place:
        if bestRun.place<=10:
            resp['userTotalTopTenCount']=user.bestruns.exclude(place=None).count()
        if bestRun.place==1:
            resp['userTotalWRCount']=user.bestruns.filter(place=1).count()
    return resp

def adjustPlaces(user, race):
    #we know bestRun is in the top 10.
    bestRuns=PlaceHelpers.getTopTen(race, extra=True)
    ii=1
    userRun=None
    for bestRun in bestRuns:
        if ii<=10:
            useii=ii
        else:
            useii=None
        if bestRun.place != useii:
            bestRun.place = useii
            bestRun.save()
        if bestRun.user==user:
            userRun=bestRun
        ii=ii+1
    return userRun


def userFinishedRun(userId, startId, endId, raceMilliseconds, playerIds):
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    start=util.tryGet(Sign, {'signId':startId})
    if not start:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(startId)})
    end=util.tryGet(Sign, {'signId':endId})
    if not end:
        return JsonResponse({'error':True,'message':'no such sign %s'%str(endId)})
    race, createdRace=Race.objects.get_or_create(start=start, end=end)
    actionResults=[]
    if createdRace:
        actionResults.append(makeArForCreatedRace(user, race))

    raceMilliseconds=math.ceil(int(raceMilliseconds))
    run=Run(user=user, race=race, raceMilliseconds=raceMilliseconds)
    run.save()
    resp=maybeCreateBestRun(user, run)
    if 'place' in resp and resp['place']:
        #add place onto the run too, for convenience
        run.place=resp['place']
        run.save()
    if resp['place']==1 and resp['improvedPlace']: #bit annoying that they can farm TIX by gradually improving WR time.
        #grant new tixtransaction.
        actionResults.extend(makeArsForImprovedPlace(user, race))

    #if resp['improvedPlace']:
    otherPlayerIds = set([int(p) for p in playerIds.split(',') if int(p)!=userId])

    #always notify if you push these guys down.
    otherPlayerIds.add(90115385) #brou
    otherPlayerIds.add(164062733) #verv

    if int(userId) in otherPlayerIds:
        otherPlayerIds.remove(int(userId))

    top10=PlaceHelpers.getTopTen(race, extra=True)
    ars=makeRelativeActionResult(user, resp, top10, otherPlayerIds, race)
    if ars:
        actionResults.extend(ars)

    eventArs = RaceEventHelpers.EvaluateRunForEvents(run)
    if eventArs:
        actionResults.extend(eventArs)

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

def postEndpoint(request, data):
    method=request.POST.get('method') 
    if method=='userFinishedRun':
        userId=request.POST.get('userId')
        playerIds=request.POST.get('playerIds')
        startId=request.POST.get('startId')
        endId=request.POST.get('endId')
        raceMilliseconds=request.POST.get('raceMilliseconds')
        return userFinishedRun(userId=userId, playerIds=playerIds, endId=endId, startId=startId,raceMilliseconds=raceMilliseconds)
