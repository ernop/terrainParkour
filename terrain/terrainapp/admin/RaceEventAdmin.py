from django import forms

from admin_helpers import *
from allmodels import *

import util

class RaceEventAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RaceEventAdminForm, self).__init__(*args, **kwargs)
        self.fields['race'].queryset=Race.objects.order_by('start__name','end__name')
        self.fields['badge'].queryset=Badge.objects.order_by('name')

class RaceEventAdmin(OverriddenModelAdmin):
    form = RaceEventAdminForm
    list_display='id active mydesc myuserdescription myrace myruns mystartdate myenddate mybadge'.split()
    list_filter=['active',]
    actions=['make_active', 'make_inactive', 'make_permanent',]

    def make_active(self, request, queryset):
        for el in queryset:
            el.active=True
            el.save()

    def make_inactive(self, request, queryset):
        for el in queryset:
            el.active=False
            el.save()

    def make_permanent(self, request, queryset):
        perm=RaceEventType.objects.get(name='permanent')
        for el in queryset:
            el.eventtype=el
            el.save()

    def mydesc(self, obj):
        return '%s<br>%s'%(obj.name, obj.description)

    def myrace(self,obj):
        return obj.race.clink()

    def mystartdate(self,obj):
        return util.safeDateAsString(obj.startdate)

    def myenddate(self,obj):
        return util.safeDateAsString(obj.enddate)

    def mybadge(self, obj):
        if obj.badge:
            return obj.badge.clink()
        return '-'

    def myuserdescription(self, obj):
        return obj.GetEventDescription()

    def myruns(self, obj):
        return '<a href="../run/?race__id__exact=%d">%d</a>'%(obj.race.id, obj.race.runs.count())

    def mytixtransactions(self, obj):
        tt=TixTransactions.filter()


    adminify(mydesc, myrace, mystartdate, myenddate, mybadge, myuserdescription, myruns)

