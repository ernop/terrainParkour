from admin_helpers import *
from allmodels import *

import util

class BadgeGrantAdmin(OverriddenModelAdmin):
    list_display='id myuser mybadge'.split()

    def myuser(self, obj):
        return obj.user.clink()

    def mybadge(self, obj):
        return obj.badge.clink()

    adminify(myuser, mybadge)

