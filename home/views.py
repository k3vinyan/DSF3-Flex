# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from drivers.models import Driver
from routes.models import Route, Block
from datetime import datetime
import pytz
from pytz import timezone
import requests
from dsf3 import helpers
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup

# Create your views here.
def index(request):

    if request.method == 'GET':
        drivers = Driver.objects.all()
        routes = Route.objects.values()

        unassignRoutes = []
        assignRoutes = []
        notArrivedDrivers = []
        arrivedDrivers = []
        assignDrivers = []
        unassignClusters = {}

        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        todayHour = date.strftime('%H')


        for route in routes:
            if route['isAssigned'] == False:
                unassignRoutes.append(route)
                cluster = route['cluster']
                if cluster not in unassignClusters:
                    unassignClusters[cluster] = {'count': 1}
                else:
                    unassignClusters[cluster]['count'] += 1

        for driver in drivers:
            driverTime = driver.startTime.split(":")
            driverHour = int(driverTime[0])
            driverMin = int(driverTime[1].split(" ")[0])
            driverPeriod = driverTime[1].split(" ")[1]

            if driver.checkin == False and driver.isNoShow == True and driverHour >= todayHour:
                notArrivedDrivers.append(driver)
            elif driver.checkin == True and driver.isAssigned == False:
                arrivedDrivers.append(driver)
            elif driver.checkin == True and driver.isAssigned == True and driver.checkout == False and driver.isNoShow == False:
                assignDrivers.append(driver)


        totalUnassignRoutes =  len(unassignRoutes)
        totalAssignRoutes = len(assignRoutes)
        totalNotArrivedDrivers = len(notArrivedDrivers)
        totalArrivedDrivers = len(arrivedDrivers)
        totalAssignDrivers = len(assignDrivers)
        totalRoutes = len(routes)
        totalDrivers = len(drivers)
        totalUnassignDrivers = len(notArrivedDrivers) + len(arrivedDrivers)


        return render(request, 'home/index.html',
                {
                    'unassignRoutes':unassignRoutes,
                    'assignRoutes':assignRoutes,
                    'totalNotArrivedDrivers':totalNotArrivedDrivers,
                    'totalArrivedDrivers':totalArrivedDrivers,
                    'totalAssignDrivers':totalAssignDrivers,
                    'totalAssignRoutes':totalAssignRoutes,
                    'totalUnassignRoutes':totalUnassignRoutes,
                    'totalRoutes':totalRoutes,
                    'totalDrivers':totalDrivers,
                    'unassignClusters':unassignClusters,
                    'totalUnassignDrivers':totalUnassignDrivers,
                    'totalAssignDrivers':totalAssignDrivers
                })

