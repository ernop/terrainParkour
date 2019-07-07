import json
#all get or post calls json will have ['actionResults'], which is a list of these.  Lua will interpret them upon return.
#this doesn't cover direct data requests - just side effects of posts.
#later will have stuff like "apply reward" on client side
#which will do stuff like grant badges, once that logic is on server.

from terrain.models.ActionResultSent import ActionResultSent
from terrain.models.RobloxUser import RobloxUser

class ActionResult(object):
    def __init__(self, notify, message, userId, notifyAllExcept = False, persistent = False, kind='undefined'):
        self.notify=notify or False
        self.message=message or ''
        self.notifyAllExcept = notifyAllExcept
        self.userId = userId
        self.persistent = persistent
        self.kind=kind
        try:
            user=RobloxUser.objects.get(pk=userId)
        except:
            assert(False,'failed to find userid when logging ActionResultSent. %s'%str(userId))
            return
 
        ars=ActionResultSent(notify=notify, user=user, message=message, notifyAllExcept=notifyAllExcept)
        ars.save()

    def __repr__(self):
        return repr(self.__dict__)