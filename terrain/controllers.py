from django.http import JsonResponse
from terrainapp.models import *
import admin

def getSecretKey():
	res=open('secret.txt','r').read().strip()
	return res

secret=getSecretKey() 
noKey={'error':True,'message':'missing secret key'}

#there is a required secret key
def security(func):
	def inner(request, *kwgs):
		provided_secret=request.GET.get('secret')
		if provided_secret!=secret:
			return JsonResponse(noKey)
		return func(request, *kwgs)
	return inner

def test(request):
	return JsonResponse({"result":True, "message":'test.'})

#general user info
def getRobloxUser(request, userId):
	user=RobloxUser.objects.filter(userId=userId)
	if user.count()==0:
		res={'missing':True}
	else:
		user=user[0]
		res={'userId':user.userId,
		'username':user.username}
	return JsonResponse(res)
	
def robloxUserJoined(request, userId):
	user, created=RobloxUser.objects.get_or_create(userId=userId)
	res={'success':True}
	join=GameJoin(user=user)
	join.save()
	return JsonResponse(res)
	
def robloxUserLeft(request, userId):
	user, created=RobloxUser.objects.get_or_create(userId=userId)
	leave=GameLeave(user=user)
	leave.save()
	return JsonResponse(res)
	
def userFoundSign(request, userId, signId):
	user, created=RobloxUser.objects.get_or_create(userId=userId)
	sign=Sign.mustGet(signId=signId)
	if not sign:
		return {'error':True,'message':'no such sign %s'%str(signId)}
	find=UserFoundSign(user=user, sign=sign)
	find.save()
	return JsonResponse({'success':'true'})
	
def userFinishedRace(request ,userId, startId, endId, raceMilliseconds):
	user, created=RobloxUser.objects.get_or_create(userId=userId)
	start=Sign.mustGet(Sign, signId=startId)
	if not start:
		return {'error':True,'message':'no such sign %s'%str(startId)}
	end=Sign.mustGet(Sign, signId=endId)
	if not end:
		return {'error':True,'message':'no such sign %s'%str(endId)}
	race, created=Race.objects.get_or_create(start=start, end=end)
	race.save()
	run=Run(user=user, race=race, raceMilliseconds=raceMilliseconds)
	run.save()
	return JsonResponse({'success':'true'})