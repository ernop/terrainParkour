from enum import Enum

class TixTransactionTypeEnum(Enum):
    DAILY = 1
    NEW_WR = 2 #setting a WR
    NEW_FIND = 3 #finding a new sign
    NEW_RACE = 4 #finding a new race
    #KNOCKOUT = 5 #knocking someone out.
    #RACEEVENT_WIN = 2 #for upcoming raceevents.
