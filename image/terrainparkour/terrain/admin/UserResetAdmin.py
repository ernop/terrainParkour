from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class UserResetAdmin(OverriddenModelAdmin):
    list_display='id myuser created'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(UserResetAdmin, self).lookup_allowed(key, value)

    myuser,=adminify(myuser)

