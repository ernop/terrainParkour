import random, datetime

from django.core.management.base import BaseCommand
import util

class Command(BaseCommand):
    help = 'Create a 15 minute long race'

    def handle(self, *args, **options):
        from terrainapp.models.RaceEventTypeEnum import AUTOGENERATED_TENMINUTE
        from terrainapp.models.Race import Race
        from terrainapp.models.RaceEvent import RaceEvent
        from terrainapp.models.RaceEventType import RaceEventType
        
        race=random.choice(Race.objects.all())
        now=util.utcnow()
        name="Quick race!"
        gap = datetime.timedelta(minutes=15)
        ret = RaceEventType.objects.get(id=AUTOGENERATED_TENMINUTE)
        er = RaceEvent(name=name, race=race, startdate=now, enddate=now+gap, active=True, eventtype=ret)
        er.save()
