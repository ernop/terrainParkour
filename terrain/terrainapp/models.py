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

	
	def mustGet(**kwgs):
		try:
			res=self.objects.get(**kwgs)
		except ObjectDoesNotExist:
			res=None
		return res
	
	class Meta:
		app_label='terrainapp'
		abstract=True

class RobloxUser(BaseModel):
	userId=models.IntegerField(unique=True) #blank=True, null=True
	username=models.CharField(max_length=30)
	
	class Meta:
		app_label='terrainapp'
		db_table='robloxuser'

	def __unicode__(self):
		return self.username
		
class GameJoin(BaseModel):
	user=models.ForeignKey('RobloxUser', related_name='joins')
	
	class Meta:
		app_label='terrainapp'
		db_table='gamejoin'
		
class GameLeave(BaseModel):
	user=models.ForeignKey('RobloxUser', related_name='leaves')
	
	class Meta:
		app_label='terrainapp'
		db_table='gameleave'
		
class Sign(BaseModel):
	signid=models.IntegerField()
	name=models.CharField(max_length=50)
	
	class Meta:
		app_label='terrainapp'
		db_table='sign'
		
	def __unicode__(self):
		return 'Sign %d (%s)'%(self.signid, self.name)
		
	def __str__(self):
		return 'Sign %d (%s)'%(self.signid, self.name)
		
class Find(BaseModel):
	sign=models.ForeignKey('Sign', related_name='finds')
	user=models.ForeignKey('RobloxUser', related_name='finds')
	
	class Meta:
		app_label='terrainapp'
		db_table='find'
		
	def __unicode__(self):
		return '%s found %s'%(self.user.username, self.sign.name)
		
class Race(BaseModel):
	start=models.ForeignKey('Sign', related_name='starts')
	end=models.ForeignKey('Sign', related_name='ends')
	
	class Meta:
		app_label='terrainapp'
		db_table='race'
		
class Run(BaseModel):
	race=models.ForeignKey('Race', related_name='runs')
	user=models.ForeignKey('RobloxUser', related_name='runs')
	racemilliseconds=models.IntegerField() #run time in milliseconds
	
	class Meta:
		app_label='terrainapp'
		db_table='run'
	