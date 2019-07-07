from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class BadgeGrantAdmin(OverriddenModelAdmin):
    list_display='id myuser mybadge'.split()

    def myuser(self, obj):
        return obj.user.clink()

    def mybadge(self, obj):
        return obj.badge.clink()

    myuser, mybadge=adminify(myuser, mybadge)

