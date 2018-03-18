from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class ActionResultSent(BaseModel):
    message=models.CharField(max_length=300)
    notify=models.BooleanField()
    notifyAllExcept=models.BooleanField()
    userId=models.IntegerField()

    class Meta:
        app_label=APP
        db_table='actionresultsent'

    def __str__(self):
        return '"%s" notify:%s, except:%s, userId:%s'%(self.message, str(self.notify), str(self.notifyAllExcept), str(self.userId))

