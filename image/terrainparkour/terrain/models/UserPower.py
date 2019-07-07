#~ from django.db import models
#~ from terrainapp.basemodel import BaseModel
#~ from constants import *

#~ class UserPower(BaseModel):
    #~ user=models.ForeignKey('RobloxUser', related_name='userpowers')
    #~ power=models.ForeignKey('Power', related_name='userpowers')
    #~ day=models.ForeignKey('Day', related_name='userpowers')

    #~ class Meta:
        #~ app_label=APP
        #~ db_table='userpower'

    #~ def __str__(self):
        #~ return '%s has power %s on %s'%(self.user, self.power.name, self.day)
