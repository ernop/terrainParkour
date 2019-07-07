from django.db import models
from terrainparkour.basemodel import BaseModel
from terrainparkour.constants import *

class BadgeGrant(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='badgegrants', on_delete=models.CASCADE, db_column='user_id')
    badge=models.ForeignKey('Badge', related_name='badgegrants', on_delete=models.CASCADE, db_column='badge_id')

    class Meta:
        app_label='terrainparkour'
        db_table='badgegrant'

    def __str__(self):
        return 'badgegrant: %s %s %s'%(self.user, self.badge, self.created)
