from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class BadgeGrant(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='badgegrants')
    badge=models.ForeignKey('Badge', related_name='badgegrants')

    class Meta:
        app_label='terrainapp'
        db_table='badgegrant'

    def __str__(self):
        return 'badgegrant: %s %s %s'%(self.user, self.badge, self.created)
