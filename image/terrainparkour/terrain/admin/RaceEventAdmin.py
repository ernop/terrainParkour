from django import forms

from django.db.models import Sum

from terrainparkour.enums.RaceEventTypeEnum import *

from terrainparkour.enums.TixTransactionTypeEnum import *

from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class RaceEventAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RaceEventAdminForm, self).__init__(*args, **kwargs)
        self.fields['race'].queryset=Race.objects.order_by('start__name','end__name')
        self.fields['badge'].queryset=Badge.objects.order_by('name')

class RaceEventAdmin(OverriddenModelAdmin):
    form = RaceEventAdminForm
    list_display='id active myrunning_now mydesc myuserdescription eventtype myrace myruns myvalid_runs mytixtransactions mystartdate myenddate mybadge'.split()
    list_filter=['active', 'eventtype']
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
            el.eventtype=perm
            el.save()

    def mydesc(self, obj):
        return '%s<br>%s'%(obj.name, obj.description)

    def myrace(self,obj):
        return obj.race.clink()

    def mystartdate(self,obj):
        if not obj.startdate:
            return '-'
        return util.safeDateAsString(obj.startdate)

    def myenddate(self,obj):
        if not obj.startdate:
            return '-'
        return util.safeDateAsString(obj.enddate)

    def mybadge(self, obj):
        if obj.badge:
            return obj.badge.clink()
        return '-'

    def myuserdescription(self, obj):
        return obj.GetEventDescription(onlyTopLevel=True)

    def mytixtransactions(self, obj):
        #figure out
        #link to the same raceevent__id
        transactions=TixTransaction.objects.filter(targetType__in=TixTransactionRacePrizeAwardTypeIds,
                                                    targetId=obj.id)
        ct=transactions.count()
        total=transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        if ct==0:
            return '-'
        return '%d tix (%d)'%(total, ct)

    def myvalid_runs(self, obj):
        runs=obj.GetValidRuns()
        joined='<br>'.join(['<span class=nb style="white-space:nowrap;">%s %0.3fs %sp</span>'%(run.user.clink(), run.raceMilliseconds/1000.0, str(run.place)) for run in runs])

        return joined

    def myruns(self, obj):
        runct=obj.race.runs.count()
        return '<a href="../run/?race__id__exact=%d">%d</a>'%(obj.race.id, runct)

    def myrunning_now(self, obj):
        now=util.utcnow()
        if obj.startdate and obj.enddate:
            return obj.startdate<now and obj.enddate>now
        return True

    myrunning_now.boolean=True

    mydesc, myrace, mytixtransactions, mystartdate, myenddate, mybadge, myuserdescription, myruns, myvalid_runs, myrunning_now=adminify(mydesc, myrace, mytixtransactions, mystartdate, myenddate, mybadge, myuserdescription, myruns, myvalid_runs, myrunning_now)

