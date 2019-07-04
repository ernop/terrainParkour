from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class UserDiedAdmin(OverriddenModelAdmin):
    list_display='id myuser created x y z'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def myother(self):
        return ''

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(UserDiedAdminn, self).lookup_allowed(key, value)

    print('a')
    myuser, =adminify(myuser)


