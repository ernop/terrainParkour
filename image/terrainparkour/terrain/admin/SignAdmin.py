from terrainparkour.admin_helpers import *
from terrainparkour.allmodels import *

from terrainparkour import util

class SignAdmin(OverriddenModelAdmin):
    list_display='id signId name myfinds mynearest mystarts myends mypos created'.split()
    list_filter=['name',]
    search_fields=['name',]
    actions=['recalculate_find_totals','recalculate_nearest',]

    def myfinds(self, obj):
        return mark_safe('<a href="../find/?sign__signId__exact=%d">%d finds</a>'%(obj.signId, obj.finds.count()))

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

    myfinds, myends, mystarts, mypos, mynearest=adminify(myfinds, myends, mystarts, mypos, mynearest)
