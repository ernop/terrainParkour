from . import terrainutil

import django.utils
django.utils.timezone.activate('America/Juneau')

from django.db import models
APP='terrainapp'

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

class RequestSource(BaseModel):
    ip=models.CharField(max_length=100)
    success_count=models.IntegerField(default=0)
    failure_count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='requestsource'

    def __str__(self):
        return 'Source:%s successes: %d failures: %d'%(self.ip, self.success_count, self.failure_count)

class UserSource(BaseModel): #this is the summary of every time a user joined from this IP.
    user=models.ForeignKey('RobloxUser', related_name='usersources')
    source=models.ForeignKey('RequestSource', related_name='usersources')
    first=models.BooleanField(default=0) #whether the user started the server.
    count=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='usersource'

    def __str__(self):
        return '%s joined from ip %s %d times.'%(self.user, self.source.ip, self.count)

class FailedSecurityAttempt(BaseModel):
    source=models.ForeignKey('RequestSource', related_name='failures')
    params=models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='failedsecurityattempt'

    def __str__(self):
        return '%s failed at %s'%(self.source, self.created)

class RobloxUser(BaseModel):
    userId=models.IntegerField(unique=True) #blank=True, null=True
    username=models.CharField(max_length=30)

    class Meta:
        app_label='terrainapp'
        db_table='robloxuser'

    def __str__(self):
        return self.username or str(self.userId)

class GameJoin(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='joins')

    class Meta:
        app_label='terrainapp'
        db_table='gamejoin'

    def __str__(self):
        return '%s joined game.'%self.user.username

class UserDied(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='deaths')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userdied'

    def __str__(self):
        return '%s died in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)

class UserQuit(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='quits')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userquit'

    def __str__(self):
        return '%s quit in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)

class UserReset(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='resets')
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='userreset'

    def __str__(self):
        return '%s reset in game at %0.0f, %0.0f, %0.0f.'%(self.user.username, self.x, self.y, self.z)


class GameLeave(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='leaves')

    class Meta:
        app_label='terrainapp'
        db_table='gameleave'

    def __str__(self):
        return '%s left game.'%self.user.username

class Sign(BaseModel):
    signId=models.IntegerField()
    name=models.CharField(max_length=50)
    x=models.FloatField(blank=True, null=True)
    y=models.FloatField(blank=True, null=True)
    z=models.FloatField(blank=True, null=True)

    calcFinds=models.IntegerField(default=0) #calculated values for total finds.

    class Meta:
        app_label='terrainapp'
        db_table='sign'

    def __unicode__(self):
        return 'Sign %d (%s)'%(self.signId, self.name)

    def __str__(self):
        return '%s'%(self.name)

class Find(BaseModel):
    sign=models.ForeignKey('Sign', related_name='finds')
    user=models.ForeignKey('RobloxUser', related_name='finds')

    class Meta:
        app_label='terrainapp'
        db_table='find'

    def __str__(self):
        return '%s found %s'%(self.user.username, self.sign.name)

class Race(BaseModel):
    start=models.ForeignKey('Sign', related_name='starts')
    end=models.ForeignKey('Sign', related_name='ends')
    distance=models.IntegerField(default=0)

    class Meta:
        app_label='terrainapp'
        db_table='race'

    def calculateDistance(self):
        if self.start and self.end:
            self.distance=terrainutil.getDistance(self.start, self.end)
            self.save()

    def __str__(self):
        return '%s => %s'%(self.start.name, self.end.name)

class Run(BaseModel):
    race=models.ForeignKey('Race', related_name='runs')
    user=models.ForeignKey('RobloxUser', related_name='runs', db_index=True)
    place=models.IntegerField(default=0)

    raceMilliseconds=models.IntegerField() #run time in milliseconds

    class Meta:
        app_label='terrainapp'
        db_table='run'

    def __str__(self):
        return '%s ran the race from %s to %s in %f'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000)

class BestRun(BaseModel): #an individual user's best run of a certain race.  This is how we generate user-distinct top 10
    race=models.ForeignKey('Race', related_name='bestruns')
    user=models.ForeignKey('RobloxUser', related_name='bestruns')
    place=models.IntegerField(blank=True, null=True) #global place for this race.
    raceMilliseconds=models.IntegerField() #run time in milliseconds

    class Meta:
        app_label='terrainapp'
        db_table='bestrun'

    def __str__(self):
        placeText=self.place and '[place: %d]'%self.place
        return '%s\'s bestrun of the race from %s to %s took: %f%s'%(self.user.username, self.race.start.name, self.race.end.name, self.raceMilliseconds/1000, placeText)

class Message(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='messages')
    text=models.CharField(max_length=200)
    read=models.BooleanField(default=False)

    class Meta:
        app_label='terrainapp'
        db_table='message'

    def __str__(self):
        return 'Message %s=>%s'%(self.user, self.text)

class GameServerError(BaseModel):
    code=models.CharField(max_length=100)
    data=models.CharField(max_length=500)
    message=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='gameservererrors', blank=True, null=True)

    class Meta:
        app_label='terrainapp'
        db_table='gameservererror'

    def __str__(self):
        return '%s:%s:%s'%(self.code or '',self.data or '',self.message or '')

class ChatMessage(BaseModel):
    user=models.ForeignKey('RobloxUser', related_name='chatmessages')
    rawtext=models.CharField(max_length=500)
    filteredtext=models.CharField(max_length=500)
    requestsource=models.ForeignKey('RequestSource', related_name='chatmessages')

    class Meta:
        app_label='terrainapp'
        db_table='chatmessage'

    def __str__(self):
        fil=''
        if self.rawtext!=self.filteredtext:
            fil=' => '+self.filteredtext
        return '%s sent %s%s'%(self.user.username, self.rawtext, fil)
