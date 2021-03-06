from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *
from terrainparkour.enums.RaceEventTypeEnum import *
from .Run import Run
from .BestRun import BestRun
from terrainparkour import util

class RaceEvent(BaseModel):
    name=models.CharField(max_length=100, default='')
    description=models.CharField(max_length=1000, default='', blank=True)
    race=models.ForeignKey('Race', related_name='raceevents', on_delete=models.CASCADE)
    active=models.BooleanField(default=False) #is the event active.
    startdate=models.DateTimeField(blank=True, null=True) #if PERMANENT, then fine to be null
    enddate=models.DateTimeField(blank=True, null=True)
    badge=models.ForeignKey('Badge', related_name='raceevents', blank=True, null=True, on_delete=models.CASCADE)
    eventtype = models.ForeignKey('RaceEventType', default=None, null=True, on_delete=models.CASCADE) #like, 5 minute, permanent, etc

    class Meta:
        app_label='terrainparkour'
        db_table='raceevent'

    def __str__(self):
        badgetext=self.badge and ', and get badge %s'%self.badge.name or ''
        if self.startdate:
            datezone = '%s to %s'%(util.safeDateAsString(self.startdate), util.safeDateAsString(self.enddate))
        else:
            datezone='permanent'
        return '%s: %s%s - %s. %s'%(self.name, self.race, badgetext, datezone, self.description)

    def forUser(self):
        return self.name

    #for users
    def GetEventDescription(self, onlyTopLevel=False):
        now=util.utcnow()
        remainingtext=''

        if self.badge:
            badgetext='Badge award: "%s"!'%self.badge.name
        else:
            badgetext=''

        if self.eventtype:
            if self.eventtype.id in RaceEventTypeIdsWhichEnd:
                if not self.enddate:
                    raise
                timeTilEnd=(self.enddate-now).total_seconds()
                if timeTilEnd>0:
                    remainingtext='%s left!'%util.safeTimeIntervalAsString(timeTilEnd, onlyTopLevel)
                else:
                    remainingtext='It ended %s ago!'%util.safeTimeIntervalAsString(-1*timeTilEnd, onlyTopLevel)
        
        #this is confusing that it's showing all-time.
        br=BestRun.GetFirstPlaceBestRunForRace(self.race)
        if br   :
            leaderText='The current leader is %s, who took %0.3fs'%(br.user.username, br.raceMilliseconds/1000.0)
        else:
            leaderText='Nobody has run it yet.'

        return '%s %s %s %s %s'\
            %(self.name, 
            self.race, 
            badgetext,
            remainingtext, leaderText)

    #get runs which qualify in this interval
    def GetValidRuns(self):
        if self.eventtype.id in RaceEventTypeIdsWhichEnd:
            res=Run.objects.filter(race=self.race, created__gt=self.startdate, created__lt=self.enddate)
        else:
            res=Run.objects.filter(race=self.race)
        return res