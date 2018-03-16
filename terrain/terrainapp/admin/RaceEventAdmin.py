from admin_helpers import *
from allmodels import *

import util

class RaceEventAdmin(OverriddenModelAdmin):
    list_display='mydesc myrace mystartdate myenddate mybadge'.split()

    def mydesc(self, obj):
        return '%s<br>%s'%(obj.name, obj.description)

    def myrace(self,obj):
        return obj.race.clink()

    def mystartdate(self,obj):
        return util.safeDateAsString(obj.startdate)

    def myenddate(self,obj):
        return util.safeDateAsString(obj.enddate)

    def mybadge(self, obj):
        return obj.badge.clink()

    adminify(mydesc, myrace, mystartdate, myenddate, mybadge)

