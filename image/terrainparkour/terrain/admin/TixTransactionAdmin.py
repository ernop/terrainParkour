from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

from terrainparkour.enums.TixTransactionTypeEnum import *

class TixTransactionAdmin(OverriddenModelAdmin):
    list_display='id amount myuser myreason mytarget transactionday created'.split()
    search_fields=['user__username',]
    list_filter=['targetType',]

    def myuser(self,obj):
        return obj.user.clink()

    def myreason(self, obj):
        try:
            return TixTransactionTypeEnum[obj.targetType]
        except:
            return 'err'

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(TixTransactionAdmin, self).lookup_allowed(key, value)

    def mytarget(self, obj):
        if obj:
            targetType = TixTransactionTypeEnum[obj.targetType]
            if targetType in TixTargetTypeIsRaceEventTypes:
                raceEvent=RaceEvent.objects.get(pk=obj.targetId)
                return raceEvent.clink()
            if targetType in TixTargetTypeIsRaceTypes:
                find=Race.objects.get(pk=obj.targetId)
                return find.clink()
            if targetType in TixTargetTypeIsFindTypes:
                find=Find.objects.get(pk=obj.targetId)
                return find.clink()
            if targetType == 'dailylogin':
                return 'daily'
            else:
                return '-'
        else:
            return '(None)'

    myuser, myreason, mytarget=adminify(myuser, myreason, mytarget)


