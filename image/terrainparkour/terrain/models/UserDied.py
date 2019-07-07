from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class UserDied(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='deaths', on_delete=models.CASCADE)
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label=APP
        db_table='userdied'

    def __str__(self):
        try:
            return '%s died in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)
        except:
            return '%s died at broken location.'%self.user.username

