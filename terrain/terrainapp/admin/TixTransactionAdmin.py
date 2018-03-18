from admin_helpers import *
from allmodels import *
from TixTransactionTypeEnum import *
from TixTransactionAmountEnum import *

import util

class TixTransactionAdmin(OverriddenModelAdmin):
    list_display='id amount myuser myreason mytarget transactionday created_tz'.split()
    search_fields=['user__username',]
    list_filter=['targetType',]

    def myuser(self,obj):
        return obj.user.clink()

    def myreason(self, obj):
        try:
            return TixTransactionTypeEnum(obj.targetType).name
        except:
            return 'err'

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    def mytarget(self, obj):
        if obj:
            if TixTransactionTypeEnum(obj.targetType) in (TixTransactionTypeEnum.FIRST_TIME_RACE_IN_RACEEVENT,
                                  TixTransactionTypeEnum.FIRST_TIME_PLACE_IN_RACEEVENT,
                                  TixTransactionTypeEnum.FIRST_TIME_FIRST_IN_RACEEVENT):
                raceEvent=RaceEvent.objects.get(pk=obj.targetId)
                return raceEvent.clink()
        else:
            return '-'

    adminify(myuser, myreason, mytarget)


