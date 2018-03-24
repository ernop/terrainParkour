from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *
from terrainapp.models.RaceEventTypeEnum import *
from terrainapp.models.Run import Run
import util

class RaceEvent(BaseModel):
    name=models.CharField(max_length=100, default='')
    description=models.CharField(max_length=1000, default='', blank=True)
    race=models.ForeignKey('Race', related_name='raceevents')
    active=models.BooleanField(default=False) #is the event active.
    startdate=models.DateTimeField(blank=True, null=True) #if PERMANENT, then fine to be null
    enddate=models.DateTimeField(blank=True, null=True)
    badge=models.ForeignKey('Badge', related_name='raceevents', blank=True, null=True)
    eventtype = models.ForeignKey('RaceEventType', default=None, null=True) #like, 5 minute, permanent, etc

    class Meta:
        app_label='terrainapp'
        db_table='raceevent'

    def __str__(self):
        badgetext=self.badge and ', and get badge %s'%self.badge.name or ''
        return '%s: %s%s - %s to %s. %s'%(self.name, self.race, badgetext, util.safeDateAsString(self.startdate), util.safeDateAsString(self.enddate), self.description)

    def forUser(self):
        return self.name

    #for users
    def GetEventDescription(self, onlyTopLevel=False):
        now=util.utcnow()
        timeTilEnd=(self.enddate-now).total_seconds()
        if self.eventtype!=None and self.eventtype.id==PERMANENT:
            remainingtext=''
        else:
            remainingtext='\nIt ends in %s!'%util.safeTimeIntervalAsString(timeTilEnd, onlyTopLevel)
        if self.badge:
            badgetext='\nIf you win, you get a badge: "%s"!'%self.badge.name
        else:
            badgetext=''
        return '%s. Race: %s! %s%s'\
            %(self.name, 
            self.race, 
            badgetext,
            remainingtext)

    #get runs which qualify in this interval
    def GetValidRuns(self):
        if self.eventtype.id in [QUICK['id'], DAILY['id'], HOURLY['id']]:
            res=Run.objects.filter(race=self.race, created__gt=self.startdate, created__lt=self.enddate)
        else:
            res=Run.objects.filter(race=self.race)
        return res