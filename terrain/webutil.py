import datetime, math, os
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from allmodels import *
import admin

def logUser(userId, source, first):
    '''log this user coming from this source.'''
    user, created=RobloxUser.objects.get_or_create(userId=userId)
    userSource, created=UserSource.objects.get_or_create(user=user, source=source, first=first)
    userSource.count=userSource.count+1
    userSource.save()

def getSecretKey():
    try:
        res=open('secret.txt','r').read().strip()
    except:
        res='x'
    return res

secret=getSecretKey()
noKey={'error':True,'message':'missing secret key'}

def postSecurity(func, should_log_user_source=False, first=False):
    @csrf_exempt
    def inner(request, *kwgs):
        assert request.method=='POST'
        provided_secret=request.POST.get('secret')
        exi=RequestSource.objects.filter(ip=request.META['REMOTE_ADDR'])
        if exi.count()>0:
            source=exi[0]
        else:
            source=RequestSource(ip=request.META['REMOTE_ADDR'])
            source.save()
        if provided_secret!=secret  and not settings.LOCAL:
            failure=FailedSecurityAttempt(source=source, params=str(request.POST))
            failure.save()
            source.failure_count=source.failure_count+1
            source.save()
            return JsonResponse(noKey)
        if should_log_user_source:
            logUser(kwgs[0], source, first)
        source.success_count=source.success_count+1
        source.save()
        #add source in to args for posts.
        return func(request, source)
    return inner


def security(func, should_log_user_source=False, first=False):
    def inner(request, *kwgs):
        assert request.method=='GET'
        provided_secret=request.GET.get('secret')
        exi=RequestSource.objects.filter(ip=request.META['REMOTE_ADDR'])
        if exi.count()>0:
            source=exi[0]
        else:
            source=RequestSource(ip=request.META['REMOTE_ADDR'])
            source.save()
        if provided_secret!=secret and not settings.LOCAL:
            failure=FailedSecurityAttempt(source=source, params=request.META['QUERY_STRING'])
            failure.save()
            source.failure_count=source.failure_count+1
            source.save()
            return JsonResponse(noKey)
        if should_log_user_source:
            logUser(kwgs[0], source, first)
        source.success_count=source.success_count+1
        source.save()
        return func(request, *kwgs)
    return inner


#there is a required secret key
