from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class ActionResultSent(BaseModel):
    message=models.CharField(max_length=300)
    notifyAllExcept=models.BooleanField()
    notify=models.BooleanField()
    user=models.ForeignKey('RobloxUser', related_name='actionresultssent', default=None, on_delete=models.CASCADE)

    class Meta:
        app_label=APP
        db_table='actionresultsent'

    def __str__(self):
        return '"%s" notify:%s, except:%s, user:%s'%(self.message, str(self.notify), str(self.notifyAllExcept), str(self.user))

