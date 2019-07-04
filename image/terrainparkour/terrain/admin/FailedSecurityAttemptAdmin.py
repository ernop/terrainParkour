from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class FailedSecurityAttemptAdmin(OverriddenModelAdmin):
    list_display='id params mysource created'.split()

    def mysource(self, obj):
        print("handling obj:",obj)
        return obj.source.clink()

    mysource=adminify(mysource)

