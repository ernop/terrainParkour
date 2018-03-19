from admin_helpers import *
from allmodels import *

import util


class RaceAdmin(OverriddenModelAdmin):
    list_display='id mystart myend distance myruns mybestruns created_tz mytop10 myevents'.split()
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

    def myevents(self, obj):
        pts=[]
        link='<a href="../raceevent/?race__id__exact=%d">all %d</a>'%(obj.id, obj.raceevents.count())
        for oo in obj.raceevents.all():
            pts.append(oo.clink())
        return '<br>'.join(pts)+'<br>'+link

    adminify(mystart, myend, myruncount, myruns, mybestruns, mytop10, myevents)


