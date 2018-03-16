from admin_helpers import *
from allmodels import *

import util




class RunAdmin(OverriddenModelAdmin):
    list_display='id myuser myrace place mystart myend mytime myspeed created_tz'.split()
    list_filter=[make_null_filter('place', 'top10'),  'race__start','race__end', ] #'race',

    def mystart(self, obj):
        return obj.race.start.clink()

    def myend(self, obj):
        return obj.race.end.clink()

    def myuser(self,obj):
        return obj.user.clink()

    myuser.admin_order_field='user__username'

    def mytime(self, obj):
        exi=BestRun.objects.filter(race=obj.race, user=obj.user)
        if exi:
            best=exi[0]
            if best.raceMilliseconds==obj.raceMilliseconds:
                return '<b>%0.3f Best</b>'%(obj.raceMilliseconds*1.0/1000)
            else:
                besttext=' (best: %0.3f)'%(best.raceMilliseconds/1000)
        else:
            besttext=' best missing? weird.'
        return '%0.3f%s'%(obj.raceMilliseconds*1.0/1000, besttext)

    mytime.admin_order_field='raceMilliseconds'

    def myrace(self, obj):
        return obj.race.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', 'user__userId__exact',  ):
            return True
        return super(RunAdmin, self).lookup_allowed(key, value)

    def myspeed(self, obj):
        if not obj.speed:
            obj.save()
        return '%0.1f studs/sec'%obj.speed

    myspeed.admin_order_field='-speed'

    adminify(mystart, myend, myuser, mytime, myrace, myspeed)

