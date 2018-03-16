from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class Run(BaseModel):
    race=models.ForeignKey('Race', related_name='runs')
    user=models.ForeignKey('RobloxUser', related_name='runs', db_index=True)
    place=models.IntegerField(default=0)
    speed=models.FloatField(default=0)

    raceMilliseconds=models.IntegerField() #run time in milliseconds

    class Meta:
        app_label='terrainapp'
        db_table='run'

    def __str__(self):
        return '%s ran the race from %s to %s in %f'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000)

    def save(self, *args, **kwargs):
        self.speed=self.race.distance/1.0/self.raceMilliseconds*1000
        super(Run, self).save(*args, **kwargs)
