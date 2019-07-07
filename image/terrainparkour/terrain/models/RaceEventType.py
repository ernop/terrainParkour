from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *
from terrainparkour import util

class RaceEventType(BaseModel):
    name=models.CharField(max_length=100, default='')

    class Meta:
        app_label='terrainparkour'
        db_table='raceeventtype'

    def __str__(self):
        return '%s'%(self.name)
