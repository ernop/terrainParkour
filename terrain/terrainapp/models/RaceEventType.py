from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
import util

class RaceEventType(BaseModel):
    name=models.CharField(max_length=100, default='')

    class Meta:
        app_label='terrainapp'
        db_table='raceeventtype'

    def __str__(self):
        return '%s'%(self.name)
