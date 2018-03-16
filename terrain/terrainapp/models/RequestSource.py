from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class RequestSource(BaseModel):
    ip=models.CharField(max_length=100)
    success_count=models.IntegerField(default=0)
    failure_count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='requestsource'

    def __str__(self):
        return 'Source:%s successes: %d failures: %d'%(self.ip, self.success_count, self.failure_count)
