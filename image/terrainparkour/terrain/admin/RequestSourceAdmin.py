from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class RequestSourceAdmin(OverriddenModelAdmin):
    list_display='id ip success_count failure_count myfailures mychats myusersources created'.split()

    def myfailures(self, obj):
        return '<a href="../failedsecurityattempt/?source__id=%d">%d</a>'%(obj.id, obj.failures.count())

    def myusersources(self,obj):
        return '<a href="../usersource/?source__id=%d">%d</a>'%(obj.id, obj.usersources.count())

    def mychats(self,obj):
        return '<a href="../chatmessage/?requestsource__id=%d">%d</a>'%(obj.id, obj.chatmessages.count())

    myfailures, mychats, myusersources=adminify(myfailures, mychats, myusersources)
