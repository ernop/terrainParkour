from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class GameServerErrorAdmin(OverriddenModelAdmin):
    list_display='id code message data created'.split()
    list_filter='code message data'.split()

