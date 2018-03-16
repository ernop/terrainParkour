from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class UserSource(BaseModel): #this is the summary of every time a user joined from this IP.
    user=models.ForeignKey('RobloxUser', related_name='usersources')
    source=models.ForeignKey('RequestSource', related_name='usersources')
    first=models.BooleanField(default=0) #whether the user started the server.
    count=models.IntegerField(default=0)

    class Meta:
        app_label=APP
        db_table='usersource'

    def __str__(self):
        return '%s joined from ip %s %d times.'%(self.user, self.source.ip, self.count)

