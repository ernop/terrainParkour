from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class Badge(BaseModel):
    name=models.CharField(max_length=200)
    assetId=models.IntegerField() #the roblox assetId

    class Meta:
        app_label='terrainparkour'
        db_table='badge'

    def __str__(self):
        return 'badge: %s (%d)'%(self.name, self.assetId)
