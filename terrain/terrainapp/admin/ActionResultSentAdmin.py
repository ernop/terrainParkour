from admin_helpers import *
from allmodels import *

import util

class ActionResultSentAdmin(OverriddenModelAdmin):
    list_display='message userId notify notifyAllExcept'.split()

