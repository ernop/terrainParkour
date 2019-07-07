import random, datetime

from django.core.management.base import BaseCommand
import util
from terrainparkour.models.RaceEventTypeEnum import *

class Command(BaseCommand):
    help = 'Create a 15 minute long race'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        from terrainparkour.models.Race import Race
        from terrainparkour.models.RaceEvent import RaceEvent
        from terrainparkour.models.RaceEventType import RaceEventType
        id = int(options['id'])

        type=RaceEventTypeEnum[id]

        if type=='quick':
            name="Quick race!"
        elif type=='hourly':
            name="Hourly race!"
        elif type=='daily':
            name="Daily race!"
        else:
            return

        minutes = RaceEventLengths[type]    
        now=util.utcnow()
        race = random.choice(Race.objects.all())
        gap = datetime.timedelta(minutes=minutes)
        ret = RaceEventType.objects.get(id=id)
        er = RaceEvent(name=name, race=race, startdate=now, enddate=now+gap, active=True, eventtype=ret)
        er.save()
