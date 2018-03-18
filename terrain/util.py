import datetime, pytz, math

from django.http import JsonResponse

DATE='%Y-%m-%d'
minute=60
hour=minute*60
day=hour*24
week=day*7


def tryGet(cls, params):
    res=cls.objects.filter(**params)
    if res.count()>0:
        return res[0]
    return None

def safeDateAsString(d):
    if d:
        return datetime.datetime.strftime(d,DATE)
    return 'no date set'

def safeTimeIntervalAsString(totalSeconds):
    if totalSeconds:
        return describe_session_duration(totalSeconds)
    else:
        return 'no exact date set.'

def describe_session_duration(remainder):
    if remainder ==0 or remainder==None:
        return 'active session'

    weeks=remainder//week
    remainder=remainder-weeks*week

    days=remainder//day
    remainder=remainder-days*day

    hours=remainder//hour
    remainder=remainder-hours*hour

    minutes=remainder//minute
    remainder=remainder-minutes*minute

    seconds=remainder

    res=''
    if weeks:
        res='%d weeks '%weeks
    if days:
        res+='%d days '%days
    if hours:
        res+='%d hours '%hours
    if minutes:
        res+='%d minutes '%minutes
    if seconds:
        res+='%d seconds'%seconds

    return res.strip()

def utcnow():
    now=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    return now

def dist(s1, s2):
    distance=math.pow(math.pow(s1.x-s2.x, 2)+math.pow(s1.y-s2.y, 2)+math.pow(s1.z-s2.z, 2), 1/2)
    return distance

#def MyJsonResponse(data):
#    res={}
#    for k,v in 
#    return JsonResponse(res)

def getCardinal(place):
    if not place:
        return ''
    if place==1:
        return '1st'
    if place==2:
        return '2nd'
    if place==3:
        return '3rd'
    if place==11:
        return '11th'
    return '%sth'%str(place)
