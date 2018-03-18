from allmodels import *
from TixTransactionAmountEnum import *
from TixTransactionTypeEnum import *
import util
from ActionResult import ActionResult

def GetActiveRaceEvents():
    now=util.utcnow()
    res = RaceEvent.objects.filter(startdate__lt=now, enddate__gt=now, active=True)
    return res

#find all raceEvents which match this run
def GetQualifyingEventsByRunAndUser(run):
    active = GetActiveRaceEvents()
    match=active.filter(race=run.race)
    return match

def EvaluateRunForEvents(run):
    raceEvents = GetQualifyingEventsByRunAndUser(run)
    actionResults = []
    for raceEvent in raceEvents:
        race=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.FIRST_TIME_RACE_IN_RACEEVENT.value, targetId=raceEvent.id)
        if not race:
            ar= makeTixTransaction(TixTransactionTypeEnum.FIRST_TIME_RACE_IN_RACEEVENT, run.user, raceEvent)
            actionResults.extend(ar)

        if run.place is not None:
            place=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.FIRST_TIME_PLACE_IN_RACEEVENT.value, targetId=raceEvent.id)
            if not place:
                ar= makeTixTransaction(TixTransactionTypeEnum.FIRST_TIME_PLACE_IN_RACEEVENT, run.user,  raceEvent)
                actionResults.extend(ar)

        if run.place == 1:
            first=TixTransaction.objects.filter(targetType=TixTransactionTypeEnum.FIRST_TIME_FIRST_IN_RACEEVENT.value, targetId=raceEvent.id)
            if not first:
                ar= makeTixTransaction(TixTransactionTypeEnum.FIRST_TIME_FIRST_IN_RACEEVENT, run.user, raceEvent)
                actionResults.extend(ar)
        return actionResults

def makeTixTransaction(reason, user, raceEvent):
    actionResults=[]
    #make tix transaction
    amount = TixTransactionAmountEnum[reason.name].value
    tt = TixTransaction(user=user, amount=amount, transactionday=None, targetType=reason.value, targetId=raceEvent.id)
    tt.save()

    if reason == TixTransactionTypeEnum.FIRST_TIME_RACE_IN_RACEEVENT:
        mymessage='You got %d TIX for participating in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for participating in\n%s'%(user.username, amount, raceEvent.forUser())
    elif reason == TixTransactionTypeEnum.FIRST_TIME_PLACE_IN_RACEEVENT:
        mymessage='You got %d TIX for getting top ten in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting top ten in\n%s'%(user.username, amount, raceEvent.forUser())
    elif reason == TixTransactionTypeEnum.FIRST_TIME_FIRST_IN_RACEEVENT:
        mymessage='You got %d TIX for getting first place in\n%s'%(amount, raceEvent.forUser())
        othermessage='%s got %d TIX for getting first place in\n%s'%(user.username, amount, raceEvent.forUser())

    ar=ActionResult(notify=True, userId=user.userId, message=mymessage)
    actionResults.append(vars(ar))

    ar=ActionResult(notify=True, userId=user.userId, message=othermessage, notifyAllExcept=True)
    actionResults.append(vars(ar))
    return actionResults
