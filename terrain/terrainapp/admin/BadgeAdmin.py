from admin_helpers import *
from allmodels import *

import util

class BadgeAdmin(OverriddenModelAdmin):
    list_display='name assetId'.split()

