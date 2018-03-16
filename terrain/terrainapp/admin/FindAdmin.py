from admin_helpers import *
from allmodels import *

import util

class FindAdmin(OverriddenModelAdmin):
    list_display='id mysign myuser created_tz'.split()

    def mysign(self, obj):
        return obj.sign.clink()

    def myuser(self, obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId','sign__signId__exact', ):
            return True
        return super(FindAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mysign)

