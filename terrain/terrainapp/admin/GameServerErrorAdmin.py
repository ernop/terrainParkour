from admin_helpers import *
from allmodels import *

import util

class GameServerErrorAdmin(OverriddenModelAdmin):
    list_display='id code message data created_tz'.split()
    list_filter='code message data'.split()

