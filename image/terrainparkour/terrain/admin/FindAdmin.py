from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class FindAdmin(OverriddenModelAdmin):
    list_display='id mysign myuser created'.split()

    def mysign(self, obj):
        return obj.sign.clink()

    def myuser(self, obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId','sign__signId__exact', ):
            return True
        return super(FindAdmin, self).lookup_allowed(key, value)

    myuser, mysign=adminify(myuser, mysign)

