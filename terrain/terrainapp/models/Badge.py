from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class Badge(BaseModel):
    name=models.CharField(max_length=200)
    assetId=models.IntegerField() #the roblox assetId

    class Meta:
        app_label='terrainapp'
        db_table='badge'

    def __str__(self):
        return 'badge: %s (%d)'%(self.name, self.assetId)
