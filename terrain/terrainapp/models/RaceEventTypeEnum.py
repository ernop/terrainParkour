#these ids are the id of the raceEventType on the RaceEvent object.
RaceEventLengths={
    'quick':15,
    'hourly':60,
    'daily':1440
}

rt={
    'unused':1,
    'permanent':2,
    'standard':3, #unused.
    'quick':4,
    'hourly':5,
    'daily':6,
}

RaceEventTypeEnum={}
for k,v in rt.items():
    RaceEventTypeEnum[k]=v
    RaceEventTypeEnum[v]=k

RaceEventTypeIdsWhichEnd={
    RaceEventTypeEnum['quick'],
    RaceEventTypeEnum['hourly'],
    RaceEventTypeEnum['daily'],
}