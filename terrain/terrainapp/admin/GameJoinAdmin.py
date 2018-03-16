from admin_helpers import *
from allmodels import *

from pytz import timezone as pytz_timezone

import util


class GameJoinAdmin(OverriddenModelAdmin):
    list_display='id myuser mylength created_tz myleft'.split()
    #list_filter=active_session

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact', ):
            return True
        return super(GameJoinAdmin, self).lookup_allowed(key, value)

    def mylength(self, obj):
        return util.describe_session_duration(obj.length)

    def myleft(self, obj):
        dt = obj.left.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    adminify(myuser, mylength, myleft)
