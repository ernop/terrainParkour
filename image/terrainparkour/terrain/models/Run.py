from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class Run(BaseModel):
    race=models.ForeignKey('Race', related_name='runs', on_delete=models.CASCADE)
    user=models.ForeignKey('RobloxUser', related_name='runs', db_index=True, on_delete=models.CASCADE)
    place=models.IntegerField(default=0)
    speed=models.FloatField(default=0)

    raceMilliseconds=models.IntegerField(db_column='racemilliseconds') #run time in milliseconds

    class Meta:
        app_label='terrainparkour'
        db_table='run'

    def __str__(self):
        return '%s ran the race from %s to %s in %0.3f'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000)

    def save(self, *args, **kwargs):
        self.speed=self.race.distance/1.0/self.raceMilliseconds*1000
        super(Run, self).save(*args, **kwargs)
