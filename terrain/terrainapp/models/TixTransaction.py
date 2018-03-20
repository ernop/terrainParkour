from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
from TixTransactionTypeEnum import *
from TixTransactionAmountEnum import *
from ActionResult import *
import util

class TixTransaction(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='tixtransactions')
    amount=models.IntegerField() #gain or loss of tix to the user.
    targetType = models.IntegerField() #a TixTransactionTypeEnum.  aka the type
    targetId = models.IntegerField(blank=True, null=True) 
    #if the reason is one of the "raceEvent" types, this is the id of the event.
    #if the reason is NEW_WR, target is the race.

    transactionday=models.DateField(default=None, blank=True, null=True)


    class Meta:
        app_label=APP
        db_table='tixtransaction'

    def __str__(self):
        try:
            return '%d TIX transaction (%s) for %s.'%(self.amount, TixTransactionTypeEnum(self.targetType).name, self.user.username)
        except:
            return str(self.id)

    @classmethod #returns actionResult.
    def checkUserJoined(self, user):
        #find today's tixtransaction
        today=datetime.date.today()
        reason=TixTransactionTypeEnum.DAILY
        amount=TixTransactionAmountEnum[reason.name].value
        exi=TixTransaction.objects.filter(user=user, targetType=reason.value, transactionday=today)
        if exi:
            return None
        else:
            tt=TixTransaction(user=user, amount=amount, transactionday=today, targetType=reason.value)
            tt.save()
            message='Daily Login Bonus: %d TIX'%amount
            return ActionResult(notify=True, userId=user.userId, message=message)

    @classmethod
    def GetTixBalanceByUser(self, user):
        bal=0
        for tr in user.tixtransactions.all():
            bal+=tr.amount
        return bal

