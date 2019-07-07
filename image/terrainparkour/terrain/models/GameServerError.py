from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class GameServerError(BaseModel):
    code=models.CharField(max_length=100)
    data=models.CharField(max_length=500)
    message=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='gameservererrors', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        app_label='terrainparkour'
        db_table='gameservererror'

    def __str__(self):
        return '%s:%s:%s'%(self.code or '',self.data or '',self.message or '')
