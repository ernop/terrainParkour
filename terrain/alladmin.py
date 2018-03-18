from django.contrib import admin
from allmodels import *

from terrainapp.admin.ActionResultSentAdmin import ActionResultSentAdmin
from terrainapp.admin.BadgeAdmin import BadgeAdmin
from terrainapp.admin.BestRunAdmin import BestRunAdmin
from terrainapp.admin.ChatMessageAdmin import ChatMessageAdmin
from terrainapp.admin.FailedSecurityAttemptAdmin import FailedSecurityAttemptAdmin
from terrainapp.admin.FindAdmin import FindAdmin
from terrainapp.admin.GameJoinAdmin import GameJoinAdmin
from terrainapp.admin.GameServerErrorAdmin import GameServerErrorAdmin
#from terrainapp.admin.PowerAdmin import PowerAdmin
from terrainapp.admin.SignAdmin import SignAdmin
from terrainapp.admin.RaceAdmin import RaceAdmin
from terrainapp.admin.RaceEventAdmin import RaceEventAdmin
from terrainapp.admin.RequestSourceAdmin import RequestSourceAdmin
from terrainapp.admin.RunAdmin import RunAdmin
from terrainapp.admin.RobloxUserAdmin import RobloxUserAdmin
from terrainapp.admin.TixTransactionAdmin import TixTransactionAdmin
from terrainapp.admin.UserDiedAdmin import UserDiedAdmin
#from terrainapp.admin.UserPowerAdmin import UserPowerAdmin
from terrainapp.admin.UserResetAdmin import UserResetAdmin
from terrainapp.admin.UserSourceAdmin import UserSourceAdmin
from terrainapp.admin.UserQuitAdmin import UserQuitAdmin

admin.site.register(ActionResultSent, ActionResultSentAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BestRun, BestRunAdmin)
admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(FailedSecurityAttempt, FailedSecurityAttemptAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(GameJoin, GameJoinAdmin)
admin.site.register(GameServerError, GameServerErrorAdmin)
admin.site.register(Sign, SignAdmin)
admin.site.register(TixTransaction, TixTransactionAdmin)
admin.site.register(UserSource, UserSourceAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(RaceEvent, RaceEventAdmin)
admin.site.register(RequestSource, RequestSourceAdmin)
admin.site.register(RobloxUser, RobloxUserAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(UserDied, UserDiedAdmin)
admin.site.register(UserQuit, UserQuitAdmin)
admin.site.register(UserReset, UserResetAdmin)
