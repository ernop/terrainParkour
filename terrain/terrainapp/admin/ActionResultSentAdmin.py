from admin_helpers import *
from allmodels import *

import util

class ActionResultSentAdmin(OverriddenModelAdmin):
    list_display='message myuser notify notifyAllExcept'.split()

    def myuser(self, obj):
        return RobloxUser.objects.get(pk=obj.userId).clink()

    adminify(myuser)