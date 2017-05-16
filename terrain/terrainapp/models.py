from django.db import models

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
		return u'<a class="%s%s" title="%s" href="%s/day/%s/?id=%d">%s</a>'%(klass, tooltip, wrap, settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

	def alink(self, text=None,wrap=True):
		if wrap:
		    wrap=' nb'
		else:
		    wrap=''
		if not text:
		    text=self
		return u'<a class="btn btn-default" href="%s/day/%s/%d/">%s</a>'%(wrap,settings.ADMIN_EXTERNAL_BASE, self.__class__.__name__.lower(), self.id, text)

	class Meta:
		app_label='terrain'
		abstract=True

class RobloxUser(BaseModel):
	userId=models.IntegerField() #blank=True, null=True
	username=models.CharField(max_length=30)
	
	class Meta:
		app_label='terrainapp'
		db_table='robloxuser'

	def __unicode__(self):
		return self.username