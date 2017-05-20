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

    class Meta:
        app_label='terrainapp'
        db_table='race'

    def __str__(self):
        return '%s => %s'%(self.start.name, self.end.name)

class Run(BaseModel):
    race=models.ForeignKey('Race', related_name='runs')
    user=models.ForeignKey('RobloxUser', related_name='runs', db_index=True)

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

