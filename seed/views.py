# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from routes.models import Block, Route, Tba
from drivers.models import Driver
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from seed.seedDriver import fakeDriver
from seed.seedRoute import fakeRoute

# Create your views here.

def index(request):
     return render(request, 'seed/index.html')


def seedDrivers(request):
    req = fakeDriver

    for item in req():
        
        name = item['driverName'].split(" ")
        firstName = name[0]
        lastName = name[1]

        id = item['driverId']
        startTime = item['driverStartTime']
        endTime = item['driverEndTime']
        time = item['driverBlockTime']

        try:
            Block.objects.get(startTime=startTime)
        except:
            block = Block(startTime=startTime, endTime=endTime, shiftLength=time)
            block.save()
        try:
            Driver.objects.get(DPID=id)
        except ObjectDoesNotExist:
            block = Block.objects.get(startTime=startTime)
            driver = Driver(DPID=id,
                            firstName = firstName,
                            lastName = lastName,
                            shiftLength = time,
                            startTime = startTime,
                            endTime = endTime,
                            block = block
                            )
            driver.save()
        
    return render(request, 'seed/index.html')

def seedRoutes(request):
    
        existArray = []
        noRouteArray = []
        routeCount = 0
        tbaTotal = 0
        tbaCount = 0
        
        data = fakeRoute()

        for item in data:
            print item
            tba = item['tba']
            route = item['route']
            
            try:
                r = Route.objects.get(route=route)
            except ObjectDoesNotExist:
                if route != "":
                    cluster = filter(lambda x: x.isalpha(), route)
                    routeCount += 1
                    r = Route(route=route, cluster=cluster)
                    r.save()
            try:
                tba = Tba.objects.get(tba=tba)
            except ObjectDoesNotExist:
                tbaCount += 1
                tbaTotal += 1
                
                route = item['route']
                r = Route.objects.get(route=route)
                # change status to at station for seed data
                ##status = item['status']
                status = "At Station"
                link = item['link']
                address = item['address']
                tba = Tba(route=r, tba=tba, status=status, link=link, address=address)
                tba.save()


            else:
                tbaTotal += 1
                existArray.append(tba.tba)
        existArrayLength = len(existArray)
        allRoutes = Route.objects.all()

        return render(request, 'seed/index.html')
        