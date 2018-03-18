from django.db import models
from terrainapp.basemodel import BaseModel
from constants import *

class RobloxUser(BaseModel):
    userId=models.IntegerField(unique=True) #blank=True, null=True
    username=models.CharField(max_length=30)
    banLevel=models.IntegerField(default=0) #0==safe, 1=ban, 2=bad ban

    #ban = no chat
    #superban = no chat, slow runspeed muahaha.
    def setBanLevel(self, banLevel):
        if self.banLevel!=banLevel:
            self.banLevel=banLevel
            self.save()

    class Meta:
        app_label=APP
        db_table='robloxuser'

    def __str__(self):
        bantext=''
        if self.banLevel:
            bantext='%s'%str(self.banLevel)
        return '%s%s'%(self.username or str(self.userId), bantext)
