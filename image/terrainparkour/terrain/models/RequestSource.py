from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class RequestSource(BaseModel):
    ip=models.CharField(max_length=100)
    success_count=models.IntegerField(default=0)
    failure_count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainparkour'
        db_table='requestsource'

    def __str__(self):
        return 'Source:%s successes: %d failures: %d'%(self.ip, self.success_count, self.failure_count)
