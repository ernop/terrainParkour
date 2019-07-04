from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

from .. import terrainutil

class Race(BaseModel):
    start=models.ForeignKey('Sign', related_name='starts', on_delete=models.CASCADE)
    end=models.ForeignKey('Sign', related_name='ends', on_delete=models.CASCADE)
    distance=models.IntegerField(default=0)

    class Meta:
        app_label='terrainparkour'
        db_table='race'

    def calculateDistance(self):
        if self.start and self.end:
            self.distance=terrainutil.getDistance(self.start, self.end)

    def __str__(self):
        return '%s to %s (%0.0fd)'%(self.start.name, self.end.name, self.distance)

    def save(self, *args, **kwargs):
        if not self.distance:
            self.calculateDistance()
        super(Race, self).save(*args, **kwargs)
