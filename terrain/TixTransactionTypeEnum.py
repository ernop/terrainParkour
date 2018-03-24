from enum import Enum

class TixTransactionTypeEnum(Enum):
    DAILY = 1
    NEW_WR = 2 #setting a WR
    NEW_FIND = 3 #finding a new sign
    NEW_RACE = 4 #finding a new race
    #KNOCKOUT = 5 #knocking someone out.
    #RACEEVENT_WIN = 2 #for upcoming raceevents.
    RACE = 5 #create your first run in a given raceevent.
    PLACE = 6 #first time get place <11
    FIRST = 7 #first time you get 1st place