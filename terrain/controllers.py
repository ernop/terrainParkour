from django.http import JsonResponse
from terrainapp.models import RobloxUser

def getRobloxUser(request, userId):
	import ipdb;ipdb.set_trace()
	user=RobloxUser.objects.filter(userId=userId)
	if user.count()==0:
		res={'missing':True}
	else:
		user=user[0]
		res={'userId':user.userId,
		'username':user.username}
	return JsonResponse(res)