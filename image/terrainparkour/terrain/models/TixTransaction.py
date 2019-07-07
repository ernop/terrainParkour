from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *
from terrainparkour.enums.TixTransactionTypeEnum import *
from terrainparkour.ActionResult import ActionResult
from terrainparkour import util

class TixTransaction(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='tixtransactions', on_delete=models.CASCADE)
    amount=models.IntegerField() #gain or loss of tix to the user.
    targetType = models.IntegerField() #a TixTransactionTypeEnum.  This is actually the TargetTypeID.
    targetId = models.IntegerField(blank=True, null=True) 
    #if the reason is one of the "raceEvent" types, this is the id of the event.
    #if the reason is NEW_WR, target is the race.

    transactionday=models.DateField(default=None, blank=True, null=True)

    class Meta:
        app_label=APP
        db_table='tixtransaction'

    def __str__(self):
        try:
            return '%d TIX transaction (%s) for %s.'%(self.amount, TixTransactionTypeEnum[self.targetType], self.user.username)
        except:
            return str(self.id)

    @classmethod #returns actionResult.
    def checkUserJoined(self, user):
        #find today's tixtransaction
        #import ipdb;ipdb.set_trace()
        today=datetime.date.today()
        amount=TixTransactionAmountEnum['dailylogin']
        type = TixTransactionTypeEnum['dailylogin']
        exi=TixTransaction.objects.filter(user=user, 
                                          targetType=type,
                                          transactionday=today)
        if exi:
            return None
        else:
            tt=TixTransaction(user=user, amount=amount, transactionday=today, targetType=type)
            tt.save()
            message='Daily Login Bonus: %d TIX'%amount
            return ActionResult(notify=True, userId=user.userId, message=message)

    @classmethod
    def GetTixBalanceByUser(self, user):
        bal=0
        for tr in user.tixtransactions.all():
            bal+=tr.amount
        return bal

