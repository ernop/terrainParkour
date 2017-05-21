"""terrain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from controllers import security
import controllers

urlpatterns = [
    url(r'^terrain/adminx/', admin.site.urls),
    url(r'terrain/$', security(controllers.test)),
    #gets
    #url(r'terrain/user/(-?\d+)/', security(controllers.getRobloxUser)),
    url(r'terrain/getUserSignFinds/(-?\d+)/', security(controllers.getUserSignFinds)),

    #actions
    url(r'terrain/userJoined/(-?\d+)/([\w ]+)',security(controllers.robloxUserJoined)),
    url(r'terrain/userLeft/(-?\d+)/',security(controllers.robloxUserLeft)),
    url(r'terrain/userFoundSign/(-?\d+)/(\d+)/',security(controllers.userFoundSign)),
    url(r'terrain/userFinishedRace/(-?\d+)/(\d+)/(\d+)/(\d+)', security(controllers.userFinishedRace)),
    url(r'terrain/setSignPosition/(\d+)/([\w ]+)/([\-\d\.]+)/([\-\d\.]+)/([\-\d\.]+)', security(controllers.setSignPosition)),

    #stats
    url(r'terrain/getTotalRunCount/',security(controllers.getTotalRunCount)),
    url(r'terrain/getTotalRaceCount/',security(controllers.getTotalRaceCount)),
    url(r'terrain/getTotalFindCountBySign/(\d+)/',security(controllers.getTotalFindCountBySign)),
    url(r'terrain/getTotalFindCountByUser/(-?\d+)/',security(controllers.getTotalFindCountByUser)),
    url(r'terrain/getTotalWorldRecordCountByUser/(\d+)/',security(controllers.getTotalWorldRecordCountByUser)),
    url(r'terrain/getTotalTopTenCountByUser/(\d+)/',security(controllers.getTotalTopTenCountByUser)),

    url(r'terrain/getTotalRunCountByDay/',security(controllers.getTotalRunCountByDay)),
    url(r'terrain/getTotalRaceCountByDay/',security(controllers.getTotalRaceCountByDay)),
    url(r'terrain/getTotalRunCountByUserAndDay/(-?\d+)/',security(controllers.getTotalRunCountByUserAndDay)),
    url(r'terrain/getTotalFindCountByDay/',security(controllers.getTotalFindCountByDay)),

    url(r'terrain/getTotalRunCountByUserAndRace/(-?\d+)/(\d+)/(\d+)/',security(controllers.getTotalRunCountByUserAndRace)),
    url(r'terrain/getTotalRunCountByUser/(-?\d+)/',security(controllers.getTotalRunCountByUser)),
    url(r'terrain/getTotalRunCountByRace/(\d+)/(\d+)/',security(controllers.getTotalRunCountByRace)),
    url(r'terrain/getRaceInfoByUser/(-?\d+)/(\d+)/(\d+)',security(controllers.getRaceInfoByUser)),
    url(r'terrain/getTotalRaceCountByUser/(-?\d+)/',security(controllers.getTotalRaceCountByUser)),

    url(r'terrain/getBestTimesByRace/(\d+)/(\d+)/',security(controllers.getBestTimesByRace)),
]


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse
from django.http import HttpResponse

import logging, traceback

def handler404(request):
    #response.status_code = 404
    logging.error("404: %s", request.path)
    return HttpResponse(status=200)


def handler500(request):
    #response.status_code = 500
    logging.error(traceback.format_exc())
    return HttpResponse(status=200)


