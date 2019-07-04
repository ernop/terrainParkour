from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class Power(BaseModel):
    name=models.CharField(max_length=50)

    class Meta:
        app_label=APP
        db_table='power'

    def __str__(self):
        return 'power: %s'%(self.name)

