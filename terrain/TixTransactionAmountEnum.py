from enum import Enum

class TixTransactionAmountEnum(Enum):
    DAILY = 12
    #RACE_WIN = 2
    NEW_WR = 2
    NEW_FIND = 1
    NEW_RACE = 1
    #KNOCKOUT = 1
    FIRST_TIME_RACE_IN_RACEEVENT = 2
    FIRST_TIME_PLACE_IN_RACEEVENT = 16
    FIRST_TIME_FIRST_IN_RACEEVENT = 50
