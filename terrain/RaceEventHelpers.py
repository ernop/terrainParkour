import logging

from allmodels import *
from TixTransactionAmountEnum import *
from TixTransactionTypeEnum import *
import util
from ActionResult import ActionResult
from terrainapp.models.RaceEventTypeEnum import *

logger = logging.getLogger(__name__)

def GetQuickRaceEvents():
    now=util.utcnow()
    res = RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now, active=True)
    return res

def GetActiveRaceEvents():
    res1=RaceEvent.objects.filter(active=True, eventtype__id=PERMANENT)
    now=util.utcnow()
    res2 = RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now, active=True)
    return res1|res2

#find all raceEvents which match this run
def GetQualifyingEventsByRunAndUser(run):
    active = GetActiveRaceEvents()
    match=active.filter(race=run.race)
    return match

def GetQualifyingEventsBySign(sign):
    active = GetActiveRaceEvents()
    match=active.filter(race__start=sign)
    return match

def EvaluateRunForEvents(run):
    raceEvents = GetQualifyingEventsByRunAndUser(run)
    actionResults = []
    for raceEvent in raceEvents:
        race=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.RACE.value, targetId=raceEvent.id, user__id=run.user.id)
        if raceEvent.eventtype_id==QUICK['id']:
            rewardData=QUICK['reward']
        elif raceEvent.eventtype_id==HOURLY['id']:
            rewardData=HOURLY['reward']
        elif raceEvent.eventtype_id==DAILY['id']:
            rewardData=DAILY['reward']

        if not race:
            amount=rewardData['run']
            ar = makeTixTransaction(TixTransactionTypeEnum.RACE, run.user, amount, raceEvent)
            actionResults.extend(ar)

        if run.place is not None:
            place=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.PLACE.value, targetId=raceEvent.id, user__id=run.user.id)
            if not place:
                amount=rewardData['place']
                logger.info("awarding place award because place was: %d"%run.place)
                ar= makeTixTransaction(TixTransactionTypeEnum.PLACE, run.user,  amount, raceEvent)
                actionResults.extend(ar)

        if run.place == 1:
            first=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.FIRST.value, targetId=raceEvent.id, user__id=run.user.id)
            if not first:
                amount=rewardData['first']
                ar= makeTixTransaction(TixTransactionTypeEnum.FIRST, run.user, amount, raceEvent)
                actionResults.extend(ar)
        return actionResults

def makeTixTransaction(reason, user, amount, raceEvent):
    actionResults=[]
    #make tix transaction
    tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=reason.value, targetId=raceEvent.id)
    tt.save()

    if reason == TixTransactionTypeEnum.RACE:
        mymessage='You got %d TIX for participating in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for participating in\n%s'%(user.username, amount, raceEvent.forUser())
    elif reason == TixTransactionTypeEnum.PLACE:
        mymessage='You got %d TIX for getting top ten in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting top ten in\n%s'%(user.username, amount, raceEvent.forUser())
    elif reason == TixTransactionTypeEnum.FIRST:
        mymessage='You got %d TIX for getting first place in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting first place in\n%s'%(user.username, amount, raceEvent.forUser())

    ar=ActionResult(notify=True, userId=user.userId, message=mymessage)
    actionResults.append(vars(ar))

    ar=ActionResult(notify=True, userId=user.userId, message=othermessage, notifyAllExcept=True)
    actionResults.append(vars(ar))
    return actionResults
