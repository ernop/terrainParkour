from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class Message(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='messages')
    text=models.CharField(max_length=200)
    read=models.BooleanField(default=False)

    class Meta:
        app_label='terrainapp'
        db_table='message'

    def __str__(self):
        return 'Message %s=>%s'%(self.user, self.text)
