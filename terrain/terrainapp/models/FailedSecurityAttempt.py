from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class FailedSecurityAttempt(BaseModel):
    source=models.ForeignKey('RequestSource', related_name='failures')
    params=models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label=APP
        db_table='failedsecurityattempt'

    def __str__(self):
        return '%s failed at %s'%(self.source, self.created)

