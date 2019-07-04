from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *
class Find(BaseModel):
    sign=models.ForeignKey('Sign', related_name='finds', on_delete=models.CASCADE)
    user=models.ForeignKey('RobloxUser', related_name='finds', on_delete=models.CASCADE)

    class Meta:
        app_label='terrainparkour'
        db_table='find'

    def __str__(self):
        return '%s found %s'%(self.user.username, self.sign.name)

