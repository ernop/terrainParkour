from admin_helpers import *
from allmodels import *

import util



class FailedSecurityAttemptAdmin(OverriddenModelAdmin):
    list_display='id params mysource created_tz'.split()

    def mysource(self,obj):
        return obj.source.clink()

    adminify(mysource)

