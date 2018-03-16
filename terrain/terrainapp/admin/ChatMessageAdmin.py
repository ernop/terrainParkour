from admin_helpers import *
from allmodels import *

import util


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

