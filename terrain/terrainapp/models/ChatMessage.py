from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class ChatMessage(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='chatmessages')
    rawtext=models.CharField(max_length=500)
    filteredtext=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='chatmessages')

    class Meta:
        app_label='terrainapp'
        db_table='chatmessage'

    def __str__(self):
        fil=''
        if self.rawtext!=self.filteredtext:
            fil=' => '+self.filteredtext
        return '%s sent %s%s'%(self.user.username, self.rawtext, fil)

