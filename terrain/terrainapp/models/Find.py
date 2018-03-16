from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class Find(BaseModel):
    sign=models.ForeignKey('Sign', related_name='finds')
    user=models.ForeignKey('RobloxUser', related_name='finds')

    class Meta:
        app_label='terrainapp'
        db_table='find'

    def __str__(self):
        return '%s found %s'%(self.user.username, self.sign.name)

