from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
import util

class GameJoin(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='joins')
    length=models.IntegerField(default=0) #the number of seconds til the next game leave
    left = models.DateTimeField(default=EPOCH)

    @classmethod
    def playerLeft(self, userId, leavetime):
        last_join=GameJoin.objects.filter(user__userId=userId, created__lte=leavetime).order_by('-created')
        if last_join:
            lj = last_join[0]
            lj.left=leavetime
            lj.length=(leavetime-lj.created).total_seconds()
            lj.save()

    class Meta:
        app_label=APP
        db_table='gamejoin'

    def __str__(self):
        return '%s joined game (%s).'%(self.user.username, util.describe_session_duration(self.length))

