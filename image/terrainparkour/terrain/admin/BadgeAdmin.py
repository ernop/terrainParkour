from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class BadgeAdmin(OverriddenModelAdmin):
    list_display='name assetId mygrants'.split()

    def mygrants(self, obj):
        return '<a href=../badgegrant/?badge__id=%d>%d grants</a>'%(obj.id, obj.badgegrants.count())

    mygrants,=adminify(mygrants)
