import math

from django.contrib import admin
from django.conf import settings

from terrainapp.models import *
from admin_helpers import *
from allmodels import *
from alladmin import *


admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(RobloxUser, RobloxUserAdmin)

admin.site.register(Sign, SignAdmin)
admin.site.register(Find, FindAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(BestRun, BestRunAdmin)

admin.site.register(GameJoin, GameJoinAdmin)
admin.site.register(UserDied, UserDiedAdmin)
admin.site.register(UserQuit, UserQuitAdmin)
admin.site.register(UserReset, UserResetAdmin)

admin.site.register(RequestSource, RequestSourceAdmin)
admin.site.register(FailedSecurityAttempt, FailedSecurityAttemptAdmin)
admin.site.register(UserSource, UserSourceAdmin)
admin.site.register(GameServerError, GameServerErrorAdmin)

admin.site.register(Badge, BadgeAdmin)
admin.site.register(RaceEvent, RaceEventAdmin)
