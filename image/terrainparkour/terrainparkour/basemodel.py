from django.db import models
from .constants import *

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def clink(self, text=None,wrap=True,skip_btn=False,klasses=None, tooltip=None):
        if skip_btn:
            klass=''
        else:
            klass='btn btn-default'
        if klasses:
            klass+=' '.join(klasses)
        if wrap:
            wrap=''
        else:
            wrap=' nb'
        if not text:
            text=self
        if not tooltip:
            tooltip=''

        return u'<a class="%s%s" title="%s" href="../../%s/%s/?id=%d">%s</a>'%(klass, wrap, tooltip, APP, self.__class__.__name__.lower(), self.id, text)

    class Meta:
        app_label=APP
        abstract=True

