from terrainparkour.allmodels import *

def getTopTen(race, extra=False):
    lim=10
    if extra:
        lim=11
    res=BestRun.objects.filter(race=race).order_by('raceMilliseconds')[:lim]
    return res
