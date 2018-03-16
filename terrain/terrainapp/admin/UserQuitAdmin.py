from admin_helpers import *
from allmodels import *

import util

class UserQuitAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz x y z'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(UserQuitAdmin, self).lookup_allowed(key, value)

    adminify(myuser)


