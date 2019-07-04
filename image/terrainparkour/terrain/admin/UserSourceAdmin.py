from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class UserSourceAdmin(OverriddenModelAdmin):
    list_display='id myuser first mysource count created'.split()
    search_fields=['user__username',]

    def myuser(self,obj):
        return obj.user.clink()

    def mysource(self,obj):
        return obj.source.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    myuser, mysource=adminify(myuser, mysource)


