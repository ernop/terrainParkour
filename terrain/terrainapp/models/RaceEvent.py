from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
import util

class RaceEvent(BaseModel):
    name=models.CharField(max_length=100, default='')
    description=models.CharField(max_length=1000, default='')
    race=models.ForeignKey('Race', related_name='raceevents')
    active=models.BooleanField(default=False) #is the event active.
    startdate=models.DateTimeField()
    enddate=models.DateTimeField()
    badge=models.ForeignKey('Badge', related_name='raceevents')

    class Meta:
        app_label='terrainapp'
        db_table='raceevent'

    def __str__(self):
        return 'event: %s. Race: %s and get badge: %s.  Start:%s End:%s. %s'%(self.name, self.race, self.badge.name, util.safeDateAsString(self.startdate), util.safeDateAsString(self.enddate), self.description)

    def forUser(self):
        return self.name