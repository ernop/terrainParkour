import math

from django.contrib import admin
from django.conf import settings

from terrainapp.models import *
from admin_helpers import *
import util

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
    list_display='id userId myplaytime mybanLevel username created_tz myjoins myleaves mychats myquits mysources mydeaths myruns myfinds mybestruns mytoptens mywrs'.split()
    search_fields=['username',]
    list_filter=['banLevel',]

    actions=['unban_users', 'softban_users', 'hardban_users',]

    def unban_users(self, request, queryset):
        for obj in queryset:
            obj.setBanLevel(0)

    def softban_users(self, request, queryset):
        for obj in queryset:
            obj.setBanLevel(1)

    def hardban_users(self, request, queryset):
        for obj in queryset:
            obj.setBanLevel(2)

    def mychats(self, obj):
        return '<a href="../chatmessage?user__userId=%d">%d</a>'%(obj.userId, obj.chatmessages.count())

    def myfinds(self, obj):
        return '<a href="../find?user__userId=%d">%d</a>'%(obj.userId, obj.finds.count())

    def myjoins(self, obj):
        return '<a href="../gamejoin/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.joins.count())

    def mybanLevel(self, obj):
        if obj.banLevel==0: return ''
        if obj.banLevel==1: return 'Soft Ban'
        if obj.banLevel==2: return 'Hard Ban'
        return 'Broken Banlevel: %s'%str(obj.banLevel)

    def myleaves(self, obj):
        return '<a href="../gameleave/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.leaves.count())

    def myquits(self, obj):
        return '<a href="../userquit/?user__userId__exact=%d">%d</a>'%(obj.userId, obj.quits.count())

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

    def myplaytime(self, obj):
        total=0
        for join in obj.joins.all():
            total+=join.length
        return util.describe_session_duration(total)

    adminify(myjoins, myleaves, myplaytime, mybanLevel, mychats, myquits, mysources, mydeaths, myruns, myfinds, mybestruns, mywrs, mytoptens)

class SignAdmin(OverriddenModelAdmin):
    list_display='id signId name myfinds mynearest mystarts myends mypos'.split()
    list_filter=['name',]
    search_fields=['name',]
    actions=['recalculate_find_totals','recalculate_nearest',]

    def myfinds(self, obj):
        return '<a href="../find/?sign__signId__exact=%d">%d finds</a>'%(obj.signId, obj.finds.count())

    myfinds.admin_order_field='calcFinds'

    def mystarts(self, obj):
        return '<a href="../race/?start__signId=%d">%d starts</a>'%(obj.signId, Race.objects.filter(start__signId=obj.signId).count())

    def myends(self, obj):
        return '<a href="../race/?end__signId=%d">%d ends</a>'%(obj.signId, Race.objects.filter(end__signId=obj.signId).count())

    def mypos(self, obj):
        if obj.x is not None and obj.y is not None and obj.z is not None:
            return '%0.1f, %0.1f, %0.1f'%(obj.x, obj.y, obj.z)
        return ''

    def recalculate_find_totals(self, request, queryset):
        for sign in queryset:
            sign.calcFinds=sign.finds.count()
            sign.save()

    def recalculate_nearest(self, request, queryset):
        for sign in queryset:
            sign.calcNearest=sign.findNearestSign(Sign.objects.all())
            sign.save()

    def mynearest(self, obj):
        if not obj.calcNearest:
            return '-'
        dist=obj.getDistance(obj.calcNearest)
        return obj.calcNearest.clink(text='%s %d'%(obj.calcNearest.name, dist))

    adminify(myfinds, myends, mystarts, mypos, mynearest)

class RaceAdmin(OverriddenModelAdmin):
    list_display='id mystart myend distance myruns mybestruns created_tz mytop10'.split()
    list_filter='start__signId end__signId'.split()
    actions=['recalculate_distance',]

    def recalculate_distance(self, request, queryset):
        for race in queryset:
            race.calculateDistance()
            race.save()

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

    def mytop10(self,obj):
        res=''
        bestruns = obj.bestruns.exclude(place=None).order_by('raceMilliseconds')
        rows=[]
        for br in bestruns:
            rows.append('%s (%0.3f)'%(br.user.clink(), br.raceMilliseconds/1000.0 or 0))
        return '<br>'.join(rows)

    adminify(mystart, myend, myruncount, myruns, mybestruns, mytop10)

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

    adminify(myuser, mysign)

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

class DeathAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz x y z'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(DeathAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class QuitAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz x y z'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(QuitAdmin, self).lookup_allowed(key, value)

    adminify(myuser)

class ResetAdmin(OverriddenModelAdmin):
    list_display='id myuser created_tz'.split()

    def myuser(self,obj):
        return obj.user.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId__exact',):
            return True
        return super(ResetAdmin, self).lookup_allowed(key, value)

    adminify(myuser)



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

class BestRunAdmin(RunAdmin):
    list_display='id myuser myrace mystart myend mytime myspeed place created_tz'.split()

    def mytime(self, obj):
        exi=BestRun.objects.filter(race=obj.race, user=obj.user)
        return '%0.3f'%(obj.raceMilliseconds*1.0/1000)

    def myspeed(self, obj):
        if not obj.speed:
            obj.save()
        return '%0.1f studs/sec'%obj.speed

    myspeed.admin_order_field='-speed'

    adminify(mytime, myspeed)

class RequestSourceAdmin(OverriddenModelAdmin):
    list_display='id ip success_count failure_count myfailures mychats myusersources created_tz'.split()

    def myfailures(self, obj):
        return '<a href="../failedsecurityattempt/?source__id=%d">%d</a>'%(obj.id, obj.failures.count())

    def myusersources(self,obj):
        return '<a href="../usersource/?source__id=%d">%d</a>'%(obj.id, obj.usersources.count())

    def mychats(self,obj):
        return '<a href="../chatmessage/?requestsource__id=%d">%d</a>'%(obj.id, obj.chatmessages.count())

    adminify(myfailures, mychats, myusersources)

class FailedSecurityAttemptAdmin(OverriddenModelAdmin):
    list_display='id params mysource created_tz'.split()

    def mysource(self,obj):
        return obj.source.clink()

    adminify(mysource)

class UserSourceAdmin(OverriddenModelAdmin):
    list_display='id myuser first mysource count created_tz'.split()
    search_fields=['user__username',]

    def myuser(self,obj):
        return obj.user.clink()

    def mysource(self,obj):
        return obj.source.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(UserSourceAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mysource)

class ChatMessageAdmin(OverriddenModelAdmin):
    list_display='id myuser mytext created_tz mysource'.split()
    list_filter=['requestsource__ip',]

    actions=['unban_users', 'softban_users', 'hardban_users',]

    def unban_users(self, request, queryset):
        for obj in queryset:
            obj.setBanLevel(0)

    def softban_users(self, request, queryset):
        for obj in queryset:
            obj.user.setBanLevel(1)

    def hardban_users(self, request, queryset):
        for obj in queryset:
            obj.user.setBanLevel(2)

    def myuser(self,obj):
        return obj.user.clink()

    def mytext(self,obj):
        fil=''
        if obj.rawtext!=obj.filteredtext:
            fil='<br>=&gt; '+obj.filteredtext
        return '%s%s'%(obj.rawtext, fil)

    def mysource(self, obj):
        return obj.requestsource.clink()

    def lookup_allowed(self, key, value):
        if key in ('user__userId', ):
            return True
        return super(ChatMessageAdmin, self).lookup_allowed(key, value)

    adminify(myuser, mytext, mysource)

class GameServerErrorAdmin(OverriddenModelAdmin):
    list_display='id code message data created_tz'.split()
    list_filter='code message data'.split()

class BadgeAdmin(OverriddenModelAdmin):
    list_display='name assetId'.split()

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


admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(RobloxUser, RobloxUserAdmin)

admin.site.register(Sign, SignAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(BestRun, BestRunAdmin)

admin.site.register(GameJoin, GameJoinAdmin)
admin.site.register(UserDied, DeathAdmin)
admin.site.register(UserQuit, QuitAdmin)
admin.site.register(UserReset, ResetAdmin)

admin.site.register(RequestSource, RequestSourceAdmin)
admin.site.register(FailedSecurityAttempt, FailedSecurityAttemptAdmin)
admin.site.register(UserSource, UserSourceAdmin)
admin.site.register(GameServerError, GameServerErrorAdmin)

admin.site.register(Badge, BadgeAdmin)
admin.site.register(RaceEvent, RaceEventAdmin)
