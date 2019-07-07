
_ttdata={
'dailylogin':1,
'new wr':2,
'new find':3,
'new race':4,
'quick run': 5,
'quick place': 6,
'quick first': 7,
'hourly run': 8,
'hourly place': 9,
'hourly first': 10,
'daily run': 11,
'daily place': 12,
'daily first': 13,
'permanent run':14,
'permanent place':15,
'permanent first':16}

TixTransactionTypeEnum={}
for k,v in _ttdata.items():
    TixTransactionTypeEnum[k]=v
    TixTransactionTypeEnum[v]=k

TixTransactionRacePrizeAwardTypeIds={
    5,6,7,8,9,10,11,12,13,14,15,16
    }

TixTransactionAmountEnum={
'dailylogin':12,
'new wr':2,
'new find':3, #for you
'new race':4, #for you
'quick run': 2,
'quick place': 4,
'quick first': 10,
'hourly run': 3,
'hourly place': 6,
'hourly first': 15,
'daily run': 4,
'daily place': 8,
'daily first': 20,
'permanent run':5,
'permanent place':10,
'permanent first':25,
}

#a TixTransaction TargetId is pointing to a race.
TixTargetTypeIsRaceEventTypes={
    'quick run',
    'quick place',
    'quick first',
    'hourly run',
    'hourly place',
    'hourly first',
    'daily run',
    'daily place',
    'daily first',
    'permanent run',
    'permanent place',
    'permanent first',
}

TixTargetTypeIsRaceTypes = {
    'new wr',
    'new race',
    }

TixTransactionParticipationTypes={'quick run','hourly run','daily run',
                                  'permanent run',}
TixTransactionPlaceTypes={'quick place','hourly place','daily place',
                          'permanent place',}
TixTransactionFirstTypes={'quick first','hourly first','daily first',
                          'permanent first',}

TixTargetTypeIsFindTypes={'new find'}



#i should make the raceevent display mention how many played within the time interval.

#i've got both race event metadata, and tix transaction.
#how about not get by id.