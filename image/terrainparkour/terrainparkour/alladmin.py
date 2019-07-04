from django.contrib import admin as dadmin
from .allmodels import *

from terrain.admin.ActionResultSentAdmin import ActionResultSentAdmin
from terrain.admin.BadgeAdmin import BadgeAdmin
from terrain.admin.BadgeGrantAdmin import BadgeGrantAdmin
from terrain.admin.BestRunAdmin import BestRunAdmin
from terrain.admin.ChatMessageAdmin import ChatMessageAdmin
from terrain.admin.FailedSecurityAttemptAdmin import FailedSecurityAttemptAdmin
from terrain.admin.FindAdmin import FindAdmin
from terrain.admin.GameJoinAdmin import GameJoinAdmin
from terrain.admin.GameServerErrorAdmin import GameServerErrorAdmin
#from terrain.admin.PowerAdmin import PowerAdmin
from terrain.admin.SignAdmin import SignAdmin
from terrain.admin.RaceAdmin import RaceAdmin
from terrain.admin.RaceEventAdmin import RaceEventAdmin
from terrain.admin.RaceEventTypeAdmin import RaceEventTypeAdmin
from terrain.admin.RequestSourceAdmin import RequestSourceAdmin
from terrain.admin.RunAdmin import RunAdmin
from terrain.admin.RobloxUserAdmin import RobloxUserAdmin
from terrain.admin.TixTransactionAdmin import TixTransactionAdmin
from terrain.admin.UserDiedAdmin import UserDiedAdmin
#from terrain.admin.UserPowerAdmin import UserPowerAdmin
from terrain.admin.UserResetAdmin import UserResetAdmin
from terrain.admin.UserSourceAdmin import UserSourceAdmin
from terrain.admin.UserQuitAdmin import UserQuitAdmin

dadmin.site.register(ActionResultSent, ActionResultSentAdmin)
dadmin.site.register(Badge, BadgeAdmin)
dadmin.site.register(BadgeGrant, BadgeGrantAdmin)
dadmin.site.register(BestRun, BestRunAdmin)
dadmin.site.register(ChatMessage,ChatMessageAdmin)
dadmin.site.register(FailedSecurityAttempt, FailedSecurityAttemptAdmin)
dadmin.site.register(Find, FindAdmin)
dadmin.site.register(GameJoin, GameJoinAdmin)
dadmin.site.register(GameServerError, GameServerErrorAdmin)
dadmin.site.register(Sign, SignAdmin)
dadmin.site.register(TixTransaction, TixTransactionAdmin)
dadmin.site.register(UserSource, UserSourceAdmin)
dadmin.site.register(Race, RaceAdmin)
dadmin.site.register(RaceEvent, RaceEventAdmin)
dadmin.site.register(RaceEventType, RaceEventTypeAdmin)
dadmin.site.register(RequestSource, RequestSourceAdmin)
dadmin.site.register(RobloxUser, RobloxUserAdmin)
dadmin.site.register(Run, RunAdmin)
dadmin.site.register(UserDied, UserDiedAdmin)
dadmin.site.register(UserQuit, UserQuitAdmin)
dadmin.site.register(UserReset, UserResetAdmin)
