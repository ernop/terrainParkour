from admin_helpers import *
from allmodels import *
from TixTransactionTypeEnum import *
from TixTransactionAmountEnum import *

import util

class TixTransactionAdmin(OverriddenModelAdmin):
    list_display='id amount myuser myreason day created_tz'.split()
    search_fields=['user__username',]
    list_filter=['reason',]

    def myuser(self,obj):
        return obj.user.clink()

    def myreason(self, obj):
        return TixTransactionTypeEnum(obj.reason).name

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    adminify(myuser, myreason)


