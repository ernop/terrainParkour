from admin_helpers import *
from allmodels import *

import util

class UserResetAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(UserResetAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

