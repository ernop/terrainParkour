import datetime

DATE='%Y-%m-%d'

def safeDateAsString(d):
    if d:
        return datetime.datetime.strftime(d,DATE)
    return 'no date set'
