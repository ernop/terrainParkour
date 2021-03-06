from terrainparkour.enums.RaceEventTypeEnum import *
from terrainparkour.util import *

def jsonRun(r):
    res={'raceMilliseconds':r.raceMilliseconds,
        'username':r.user.username,
        'userId':r.user.userId,
        'place':r.place}
    return res

def jsonEvent(e):
    res={
        'id':e.id,
        'start':safeDateAsString(e.startdate),
        'end':safeDateAsString(e.enddate),
        'badgeAssetId':e.badge and e.badge.assetId or 0,
        'badgeId':e.badge and e.badge.id or '',
        'badgeName':e.badge and e.badge.name or '',
        'startsignId':e.race.start.signId,
        'endsignId':e.race.end.signId,
        'startSignName':e.race.start.name,
        'endSignName':e.race.end.name,
        'distance':e.race.distance,
        'name':e.name,
        'ephemeral':e.eventtype.id != RaceEventTypeEnum['permanent'] ,
        'eventDescription':e.GetEventDescription(onlyTopLevel=True)
    }
    return res

def jsonPower(power):
    res={'name':power.name,
             'id':power.id}
    return res
