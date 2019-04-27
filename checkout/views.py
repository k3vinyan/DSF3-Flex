# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from dsf3 import helpers
from bs4 import BeautifulSoup
from django.template.defaulttags import register
from routes.models import Tba, Route
from collections import OrderedDict
from drivers.models import Driver
from checkout.models import RoutingtoolsRoute
from datetime import datetime
from dsf3 import helpers

# Create your views here.
def index(request):

    routingTools = RoutingtoolsRoute.objects.all();
    drivers = Driver.objects.filter(checkin=True).filter(isAssigned=True).filter(checkout=False)
    routes = Route.objects.filter(isAssigned=True)

    if request.method == 'GET':
        return render(request, 'checkout/index.html', {'routingTools': routingTools, 'drivers': drivers, 'routes': routes})

    #POST request
    if request.method == 'POST':

        #get time
        def getTime():
            date_format='%H:%M:%S %Z'
            date = datetime.now(tz=pytz.utc)
            date = date.astimezone(timezone('US/Pacific'))
            return date.strftime(date_format)

        driver_id = request.POST.get('driver_id')
        driver = Driver.objects.get(id=driver_id)
        if driver.checkout == False:
            driver.checkout = True
            driver.checkoutTime = helpers.getTime()
            driver.save(update_fields=['checkoutTime'])
            driver.save(update_fields=['checkout'])
        else:
            driver.checkout = False
            driver.save(update_fields=['checkout'])

    return HttpResponse(request)


def routingTools(request):
    return render(request, 'checkout/routingtool.html')
