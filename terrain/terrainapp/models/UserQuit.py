from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class UserQuit(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='quits')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userquit'

    def __str__(self):
        return '%s quit in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)
