import math

from django.contrib import admin
from django.conf import settings

from terrainapp.models import *
from admin_helpers import *
from pytz import timezone as pytz_timezone

def dist(s1, s2):
    distance=math.pow(math.pow(s1.x-s2.x, 2)+math.pow(s1.y-s2.y, 2)+math.pow(s1.z-s2.z, 2), 1/2)
    return distance

ct=0
if False:
    for s1 in Sign.objects.all():
        #if s1.signId!=2:continue
        for s2 in Sign.objects.all():
            if s1.signId==s2.signId:continue
            if s1.x and s2.x:
                distance=dist(s1, s2)
                if distance<1200:
                    #print('%d,%d'%(s1.signId, s2.signId))
                    print('%s %s %0.0f'%(s1, s2, distance))
                    ct=ct+1
                    print(ct)

class RobloxUserAdmin(OverriddenModelAdmin):
    list_display='id userId username created_tz myjoins myleaves mysources mydeaths myruns myfinds mybestruns mytoptens mywrs'.split()
    search_fields=['username',]

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def myfinds(self, obj):
        return '<a href="../find?user__userId=%d">%d</a>'%(obj.userId, obj.finds.count())

    def myjoins(self, obj):
        return '<a href="../gamejoin/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.joins.count())

    def myleaves(self, obj):
        return '<a href="../gameleave/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.leaves.count())

    def mydeaths(self, obj):
        return '<a href="../userdied/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.deaths.count())

    def myresets(self, obj):
        return '<a href="../userreset/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.resets.count())

    def mytoptens(self, obj):
        topTens=BestRun.objects.filter(user__userId=obj.userId).exclude(place=None)
        return '<a href="../bestrun/?user__userId__exact=%d&place__exact=1">%d</a>'%(obj.userId, topTens.count())

    def mywrs(self,obj):
        wrs=BestRun.objects.filter(place=1, user__userId=obj.userId)
        return '<a href="../bestrun/?user__userId__exact=%d&place__exact=1">%d</a>'%(obj.userId, wrs.count())

    def myruns(self, obj):
        return '<a href="../run?user__userId=%d">%d</a>'%(obj.userId, obj.runs.count())

    def mybestruns(self, obj):
        return '<a href="../bestrun?user__userId=%d">%d</a>'%(obj.userId, obj.bestruns.count())

    def mysources(self, obj):
        return '<a href="../usersource?user__userId=%d">%d</a>'%(obj.userId, obj.usersources.count())

    adminify(myjoins, myleaves, mysources, mydeaths, myruns, myfinds, mybestruns, mywrs, mytoptens)

class SignAdmin(OverriddenModelAdmin):
    list_display='id signId name myfinds  mystarts myends mypos'.split()
    list_filter=['name',]

    def myfinds(self, obj):
        return '<a href="../find/?sign__signId__exact=%d">%d finds</a>'%(obj.signId, obj.finds.count())

    def mystarts(self, obj):
        return '<a href="../race/?start__signId=%d">%d starts</a>'%(obj.id, Race.objects.filter(start__signId=obj.signId).count())

    def myends(self, obj):
        return '<a href="../race/?end__signId=%d">%d ends</a>'%(obj.id, Race.objects.filter(end__signId=obj.signId).count())

    def mypos(self, obj):
        if obj.x is not None and obj.y is not None and obj.z is not None:
            return '%0.1f, %0.1f, %0.1f'%(obj.x, obj.y, obj.z)
        return ''

    adminify(myfinds, myends, mystarts, mypos)

class RaceAdmin(OverriddenModelAdmin):
    list_display='id mystart myend myruncount myruns mybestruns created_tz'.split()
    list_filter='start__signId end__signId'.split()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

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
    list_display='id mysign myuser created_tz'.split()

    def mysign(self, obj):
        return obj.sign.clink()

    def myuser(self, obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId','sign__signId__exact', ):
            return True
        return super(FindAdmin, self).lookup_allowed(key, value)

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    created_tz.short_description = 'Created'

    adminify(myuser, mysign)

class GameLeaveAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(GameLeaveAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class DeathAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz x y z'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(DeathAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class ResetAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(ResetAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class GameJoinAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz'.split()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact', ):
            return True
        return super(GameJoinAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class RunAdmin(OverriddenModelAdmin):
    list_display='id myuser myrace mystart myend mytime created_tz'.split()
    list_filter=[make_null_filter('place', 'top10'), 'race', 'race__start','race__end', ]

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

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

    adminify(mystart, myend, myuser, mytime, myrace)

class BestRunAdmin(RunAdmin):
    list_display='id myuser myrace mystart myend mytime place created_tz'.split()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def mytime(self, obj):
        exi=BestRun.objects.filter(race=obj.race, user=obj.user)
        return '%0.3f'%(obj.raceMilliseconds*1.0/1000)

class RequestSourceAdmin(OverriddenModelAdmin):
    list_display='id ip success_count failure_count myfailures myusersources created_tz'.split()

    def myfailures(self, obj):
        return '<a href="../failedsecurityattempt/?source__id=%d">%d</a>'%(obj.id, obj.failures.count())

    def myusersources(self,obj):
        return '<a href="../usersource/?source__id=%d">%d</a>'%(obj.id, obj.usersources.count())

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    adminify(myfailures, myusersources)

class FailedSecurityAttemptAdmin(OverriddenModelAdmin):
    list_display='id params mysource created_tz'.split()

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def mysource(self,obj):
        return obj.source.clink()

    adminify(mysource)

class UserSourceAdmin(OverriddenModelAdmin):
    list_display='id myuser first mysource count'.split()
    list_filter=['first',]
    search_fields=['user__username',]

    def created_tz(self, obj):
        dt = obj.created.astimezone(pytz_timezone(settings.ADMIN_TIMEZONE))
        return dt.strftime(settings.DATE_FORMAT)

    def myuser(self,obj):
        return obj.user.clink()

    def mysource(self,obj):
        return obj.source.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mysource)

admin.site.register(RobloxUser, RobloxUserAdmin)

admin.site.register(Sign, SignAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(BestRun, BestRunAdmin)

admin.site.register(GameLeave, GameLeaveAdmin)
admin.site.register(GameJoin, GameJoinAdmin)
admin.site.register(UserDied, DeathAdmin)
admin.site.register(UserReset, ResetAdmin)

admin.site.register(RequestSource, RequestSourceAdmin)
admin.site.register(FailedSecurityAttempt, FailedSecurityAttemptAdmin)
admin.site.register(UserSource, UserSourceAdmin)
