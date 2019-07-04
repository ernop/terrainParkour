from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class ChatMessage(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='chatmessages', on_delete=models.CASCADE)
    rawtext=models.CharField(max_length=500)
    filteredtext=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='chatmessages', on_delete=models.CASCADE)

    class Meta:
        app_label='terrainparkour'
        db_table='chatmessage'

    def __str__(self):
        fil=''
        if self.rawtext!=self.filteredtext:
            fil=' => '+self.filteredtext
        return '%s sent %s%s'%(self.user.username, self.rawtext, fil)

