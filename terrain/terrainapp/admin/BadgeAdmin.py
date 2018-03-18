from admin_helpers import *
from allmodels import *

import util

class BadgeAdmin(OverriddenModelAdmin):
    list_display='name assetId mygrants'.split()

    def mygrants(self, obj):
        return '<a href=../badgegrant/?badge__id=%d>%d grants</a>'%(obj.id, obj.badgegrants.count())

    adminify(mygrants)
