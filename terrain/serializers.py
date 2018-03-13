from util import *

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
        'badgeAssetId':e.badge.assetId,
        'badgeId':e.badge.id,
        'badgeName':e.badge.name,
        'start_signid':e.race.start.signId,
        'end_signid':e.race.end.signId,
        'distance':e.race.distance,
    }
    return res

def jsonPower(power):
    res={'name':power.name,
             'id':power.id}
    return res
