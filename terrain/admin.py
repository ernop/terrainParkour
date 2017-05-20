from django.contrib import admin

from terrainapp.models import *
from admin_helpers import *

class RobloxUserAdmin(OverriddenModelAdmin):
    list_display='id userId username myjoins myleaves myruns myfinds mybestruns'.split()

    def myfinds(self, obj):
        return '<a href="../find?user__userId=%d">%d</a>'%(obj.userId, obj.finds.count())

    def myjoins(self, obj):
        return obj.joins.count()

    def myleaves(self, obj):
        return obj.leaves.count()

    def myruns(self, obj):
        return '<a href="../run?user__userId=%d">%d</a>'%(obj.userId, obj.runs.count())

    def mybestruns(self, obj):
        return '<a href="../bestrun?user__userId=%d">%d</a>'%(obj.userId, obj.bestruns.count())

    adminify(myjoins, myleaves, myruns, myfinds, mybestruns)

class SignAdmin(OverriddenModelAdmin):
    list_display='id signId name myfinds'.split()

    def myfinds(self, obj):
        return '%d'%(obj.finds.count())

    adminify(myfinds)

class RaceAdmin(OverriddenModelAdmin):
    list_display='id mystart myend myruncount myruns mybestruns'.split()

    def mystart(self, obj):
        return obj.start.clink()

    def myend(self, obj ):
        return obj.end.clink()

    def myruncount(self, obj):
        return obj.runs.count()

    def myruns(self, obj):
        return '<a href=../run/?race__id=%d>%d runs</a>'%(obj.id, obj.runs.count())

    def mybestruns(self, obj):
        return '<a href=../bestrun/?race__id=%d>%d bestruns</a>'%(obj.id, obj.bestruns.count())

    adminify(mystart, myend, myruncount, myruns, mybestruns)

class FindAdmin(OverriddenModelAdmin):
    list_display='id mysign myuser created'.split()

    def mysign(self, obj):
        return obj.sign.clink()

    def myuser(self, obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(FindAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mysign)

class GameLeaveAdmin(OverriddenModelAdmin):
    list_display='id myuser created'.split()

    def myuser(self,obj):
        return obj.user.clink()

    adminify(myuser)

class GameJoinAdmin(OverriddenModelAdmin):
    list_display='id myuser created'.split()

    def myuser(self,obj):
        return obj.user.clink()

    adminify(myuser)


class RunAdmin(OverriddenModelAdmin):
    list_display='id myuser myrace mystart myend mytime created'.split()
    list_filter=[make_null_filter('place', 'top10'), 'race', 'race__start','race__end', ]

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
        if key in ('user__userId', ):
            return True
        return super(RunAdmin, self).lookup_allowed(key, value)

    adminify(mystart, myend, myuser, mytime, myrace)

class BestRunAdmin(RunAdmin):
    list_display='id myuser myrace mystart myend mytime place created'.split()

    def mytime(self, obj):
        exi=BestRun.objects.filter(race=obj.race, user=obj.user)
        return '%0.3f'%(obj.raceMilliseconds*1.0/1000)





admin.site.register(RobloxUser, RobloxUserAdmin)

admin.site.register(Sign, SignAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(BestRun, BestRunAdmin)

admin.site.register(GameLeave, GameLeaveAdmin)
admin.site.register(GameJoin, GameJoinAdmin)
