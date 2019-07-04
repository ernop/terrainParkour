from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class ActionResultSentAdmin(OverriddenModelAdmin):
    list_display='message myuser notify notifyAllExcept'.split()

    def myuser(self, obj):
        return obj.user.clink()

    myuser,=adminify(myuser)
