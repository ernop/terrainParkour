from admin_helpers import *
from allmodels import *

import util

class RobloxUserAdmin(OverriddenModelAdmin):
    list_display='id userId mytix myplaytime mybanLevel username created_tz myjoins mychats myquits mysources mydeaths myruns myfinds mybestruns mytoptens mywrs'.split()
    search_fields=['username',]
    list_filter=['banLevel',]

    actions=['unban_users', 'softban_users', 'hardban_users',]

    def mytix(self, obj):
        bal = TixTransaction.GetTixBalanceByUser(obj)
        return '<a href="../tixtransaction?user__userId=%d">%d TIX (%d)</a>'%(obj.userId, bal, obj.tixtransactions.count())

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

    adminify(myjoins, mytix, myplaytime, mybanLevel, mychats, myquits, mysources, mydeaths, myruns, myfinds, mybestruns, mywrs, mytoptens)
