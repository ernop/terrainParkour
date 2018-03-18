import json
#all get or post calls json will have ['actionResults'], which is a list of these.  Lua will interpret them upon return.
#this doesn't cover direct data requests - just side effects of posts.
#later will have stuff like "apply reward" on client side
#which will do stuff like grant badges, once that logic is on server.

from terrainapp.models.ActionResultSent import ActionResultSent

class ActionResult(object):
    def __init__(self, notify, message, userId, notifyAllExcept = False):
        self.notify=notify or False
        self.message=message or ''
        self.notifyAllExcept = notifyAllExcept
        self.userId = userId
        if not userId:
            import ipdb;ipdb.set_trace()

        ars=ActionResultSent(notify=notify, userId=userId, message=message, notifyAllExcept=notifyAllExcept)
        ars.save()

    def __repr__(self):
        return repr(self.__dict__)