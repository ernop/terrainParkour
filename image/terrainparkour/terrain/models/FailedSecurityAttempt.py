from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class FailedSecurityAttempt(BaseModel):
    source=models.ForeignKey('RequestSource', related_name='failures', on_delete=models.CASCADE)
    params=models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label=APP
        db_table='failedsecurityattempt'

    def __str__(self):
        return '%s failed at %s'%(self.source, self.created)

