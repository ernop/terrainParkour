from allmodels import *
import util
from ActionResult import ActionResult
from terrainapp.models.RaceEventTypeEnum import *
from TixTransactionTypeEnum import *

#returns all quick, hourly, and daily
def getEphemeralEvents():
    now=util.utcnow()
    #get by having startdate - not exactly right.
    res = RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now, active=True,
                                   eventtype__id__in=RaceEventTypeIdsWhichEnd)
    return res

def getCurrentEvents():
    now=util.utcnow()
    #get by having startdate - not exactly right.
    permanent = RaceEvent.objects.filter(active=True,
                                   eventtype__id=RaceEventTypeEnum['permanent'])
    eph = getEphemeralEvents()
    return permanent | eph

#returns all active
def GetActiveRaceEvents():
    res1 = RaceEvent.objects.filter(active=True, eventtype__id=RaceEventTypeEnum['permanent'])
    now=util.utcnow()
    res2 = RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now, active=True)
    return res1|res2

#find all raceEvents which match this run
def GetQualifyingEventsByRun(run):
    active = GetActiveRaceEvents()
    match=active.filter(race=run.race)
    return match

def GetQualifyingEventsBySign(sign):
    active = GetActiveRaceEvents()
    match=active.filter(race__start=sign)
    return match

def EvaluateRunForEvents(run):
    raceEvents = GetQualifyingEventsByRun(run)
    actionResults = []
    for raceEvent in raceEvents:
        eventType = RaceEventTypeEnum[raceEvent.eventtype_id]
        baseTT=TixTransaction.objects.filter(targetId=raceEvent.id, user__id=run.user.id)
        
        tixTransactionType=eventType+' run'
        exi=baseTT.filter(targetType=TixTransactionTypeEnum[tixTransactionType])
        if not exi:
            amount=TixTransactionAmountEnum[tixTransactionType]
            ar = makeTixTransactionForRaceEvent(TixTransactionTypeEnum[tixTransactionType], run.user, amount, raceEvent)
            actionResults.extend(ar)

        if run.place is not None:
            tixTransactionType=eventType+' place'
            place=baseTT.filter(targetType=TixTransactionTypeEnum[tixTransactionType])
            if not place:
                amount=TixTransactionAmountEnum[tixTransactionType]
                ar = makeTixTransactionForRaceEvent(TixTransactionTypeEnum[tixTransactionType], run.user,  amount, raceEvent)
                actionResults.extend(ar)

        if run.place == 1:
            tixTransactionType=eventType+' first'
            exi = baseTT.filter(targetType=TixTransactionTypeEnum[tixTransactionType])
            if not exi:
                amount=TixTransactionAmountEnum[tixTransactionType]
                ar = makeTixTransactionForRaceEvent(TixTransactionTypeEnum[tixTransactionType], run.user, amount, raceEvent)
                actionResults.extend(ar)
        return actionResults

def makeTixTransactionForRaceEvent(tixTransactionTypeId, user, amount, raceEvent):
    actionResults=[]
    #make tix transaction
    tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=tixTransactionTypeId, targetId=raceEvent.id)
    tt.save()
    tixTransactionType=TixTransactionTypeEnum[tixTransactionTypeId]
    if tixTransactionType in TixTransactionParticipationTypes:
        mymessage='You got %d TIX for racing in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for racing in\n%s'%(user.username, amount, raceEvent.forUser())
    elif tixTransactionType in TixTransactionPlaceTypes:
        mymessage='You got %d TIX for getting top ten in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting top ten in\n%s'%(user.username, amount, raceEvent.forUser())
    elif tixTransactionType in TixTransactionFirstTypes:
        mymessage='You got %d TIX for getting first place in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting first place in\n%s'%(user.username, amount, raceEvent.forUser())

    ar=ActionResult(notify=True, userId=user.userId, message=mymessage)
    actionResults.append(vars(ar))

    ar=ActionResult(notify=True, userId=user.userId, message=othermessage, notifyAllExcept=True)
    actionResults.append(vars(ar))
    return actionResults
