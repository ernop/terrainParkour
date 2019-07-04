from django import forms

from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class RaceEventTypeAdmin(OverriddenModelAdmin):
    list_display='id name created myraceevents'.split()
    list_filter=['name',]

    def myraceevents(self, obj):
        activect=RaceEvent.objects.filter(eventtype=obj.id, active=True).count()
        inactivect=RaceEvent.objects.filter(eventtype=obj.id, active=False).count()
        return '<a href="../raceevent/?eventtype__id=%d&active=True">%d active</a>\n<a href="../raceevent/?eventtype__exact__id=%d&active=False">%d inactive</a>'%(obj.id, activect, obj.id, inactivect)

    myraceevents,=adminify(myraceevents)

