from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
import util

class RaceEvent(BaseModel):
    name=models.CharField(max_length=100, default='')
    description=models.CharField(max_length=1000, default='', blank=True)
    race=models.ForeignKey('Race', related_name='raceevents')
    active=models.BooleanField(default=False) #is the event active.
    startdate=models.DateTimeField()
    enddate=models.DateTimeField()
    badge=models.ForeignKey('Badge', related_name='raceevents', blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='raceevent'

    def __str__(self):
        badgetext=self.badge and ', and get badge %s'%self.badge.name or ''
        return '%s: %s%s - %s to %s. %s'%(self.name, self.race, badgetext, util.safeDateAsString(self.startdate), util.safeDateAsString(self.enddate), self.description)

    def forUser(self):
        return self.name

    #for users
    def GetEventDescription(self):
        now=util.utcnow()
        timeTilEnd=(self.enddate-now).total_seconds()
        remainingtext=util.safeTimeIntervalAsString(timeTilEnd)
        badgetext=self.badge and '\nIf you win, you get a badge: "%s"!'%self.badge.name or ''
        return '%s. Race: %s! %s\nIt ends in %s!'\
            %(self.name, 
            self.race, 
            badgetext,
            remainingtext)