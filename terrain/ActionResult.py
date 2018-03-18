import json
#all get or post calls json will have ['actionResults'], which is a list of these.  Lua will interpret them upon return.
#this doesn't cover direct data requests - just side effects of posts.
#later will have stuff like "apply reward" on client side
#which will do stuff like grant badges, once that logic is on server.
class ActionResult(object):
    def __init__(self, notify, message = None, notifyAllExcept = False):
        self.notify=notify or False
        self.message=message or ''
        self.notifyAllExcept = notifyAllExcept

    def __repr__(self):
        return repr(self.__dict__)