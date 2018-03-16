from admin_helpers import *
from allmodels import *

import util

class UserSourceAdmin(OverriddenModelAdmin):
    list_display='id myuser first mysource count created_tz'.split()
    search_fields=['user__username',]

    def myuser(self,obj):
        return obj.user.clink()

    def mysource(self,obj):
        return obj.source.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mysource)


