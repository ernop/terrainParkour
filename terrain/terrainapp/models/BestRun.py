from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class BestRun(BaseModel): #an individual user's best run of a certain race.  This is how we generate user-distinct top 10
    race=models.ForeignKey('Race', related_name='bestruns')
    user=models.ForeignKey('RobloxUser', related_name='bestruns')
    place=models.IntegerField(blank=True, null=True) #global place for this race.
    raceMilliseconds=models.IntegerField() #run time in milliseconds
    speed=models.FloatField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='bestrun'

    def __str__(self):
        placeText=self.place and '[place: %d]'%self.place
        return '%s\'s bestrun of the race from %s to %s took: %f%s'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000, placeText)

    def save(self, *args, **kwargs):
        self.speed=self.race.distance/1.0/self.raceMilliseconds*1000
        super(BestRun, self).save(*args, **kwargs)

