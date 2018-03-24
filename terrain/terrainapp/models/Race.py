from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

from terrainapp import terrainutil

class Race(BaseModel):
    start=models.ForeignKey('Sign', related_name='starts')
    end=models.ForeignKey('Sign', related_name='ends')
    distance=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='race'

    def calculateDistance(self):
        if self.start and self.end:
            self.distance=terrainutil.getDistance(self.start, self.end)

    def __str__(self):
        return '%s => %s (%0.0fd)'%(self.start.name, self.end.name, self.distance)

    def save(self, *args, **kwargs):
        if not self.distance:
            self.calculateDistance()
        super(Race, self).save(*args, **kwargs)
