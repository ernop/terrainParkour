from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import **

class Message(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='messages', on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    read=models.BooleanField(default=False)

    class Meta:
        app_label='terrainparkour'
        db_table='message'

    def __str__(self):
        return 'Message %s=>%s'%(self.user, self.text)
