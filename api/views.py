# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render
import requests
# from . import helpers
from bs4 import BeautifulSoup
from drivers.models import Driver
from routes.models import Block, Route, Tba
from checkout.models import RoutingtoolsRoute
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers



# Create your views here.
@csrf_exempt
def drivers(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Driver.objects.all())

        for item in req:

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




        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':

        req = json.loads(request.body)

        

        for item in req:

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

        return HttpResponse("Drivers was saved successfully!!")

@csrf_exempt
def tbas(request):
    if request.method == 'GET':

        data = serializers.serialize("json", Tba.objects.all())

        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

        for item in req:

            tba = item['tba']
            link = item['link']
            status = item['status']
            city = item['city']
            zipCode = item['zipCode']
            route = item['route']
            associate = item['associate']
            sortZone = item['sortZone']
            address = item['address']

            if route != "" or route != None:
                try:
                    Route.objects.get(route=route)
                except ObjectDoesNotExist:
                    cluster = filter(lambda x: x.isalpha(), route)
                    aRoute = Route(
                                    route=route,
                                    cluster = cluster,
                                    tbaCount = 0
                                )
                    aRoute.save()
                try:
                    Tba.objects.get(tba=tba)
                except ObjectDoesNotExist:
                    routeToUpdate = Route.objects.get(route=route)
                    tba = Tba(
                        tba=tba,
                        link=link,
                        status=status,
                        city=city,
                        route=routeToUpdate,
                        zipCode=zipCode,
                        sortZone=sortZone,
                        address=address
                    )
                    tba.save()

            else:
                tba = Tba(
                    tba=tba,
                    link=link,
                    status=status,
                    city=city,
                    zipCode=zipCode,
                    sortZone=sortZone,
                    address=address
                )
                tba.save()

                #tbaCount is updated in route app fyi

    return HttpResponse("Tbas were saved successfully!!")

@csrf_exempt
def routes(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Route.objects.all())
        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

    return HttpResponse("Routes were saved successfully!!!")

@csrf_exempt
def blocks(request):
    if request.method == 'GET':
        data = serializers.serialize("json", Block.objects.all())

        return HttpResponse(data, content_type='application/json')

    if request.method == 'POST':
        req = json.loads(request.body)

    return HttpResponse("Blocks were saved successfully!!!")

@csrf_exempt
def routingtools(request):

    if request.method == 'POST':
        routes = json.loads(request.body)

        for someRoute in routes:
            for key, value in someRoute.items():
                route = key
                cluster = filter(lambda x: x.isalpha(), route)
                for status, number in value.items():
                    if number == "" or None:
                        number = 0
                    if status == 'delivered':
                        delivered = number
                    elif status == 'attempted':
                        attempted = number
                    elif status == 'undelivered':
                        undelivered = number
                    elif status == 'depature':
                        departure = number
                    elif status == 'onRoad':
                        onRoad = number
                    elif status == 'betweenFC':
                        betweenFC = number
                    elif status == 'atStation':
                        atStation = number
                    elif status == 'other':
                        other = number

                try:
                    r = RoutingtoolsRoute.objects.get(route=route)
                    r.atStation = atStation
                    r.delivered = delivered
                    r.undelivered = undelivered
                    r.departure = departure
                    r.onRoad = onRoad
                    r.betweenFC = betweenFC
                    r.other = other
                    r.save(update_fields["atStation"])
                    r.save(update_fields["undelivered"])
                    r.save(update_fields["onRoad"])
                    r.save(update_fields["betweenFC"])
                    r.save(update_fields["other"])
                    print "route updated"
                except:
                    try:
                        r = RoutingtoolsRoute(route=route, cluster=cluster, atStation=atStation, delivered=delivered, attempted=attempted, undelivered=undelivered, departure=delivered, onRoad=onRoad, betweenFC=betweenFC, other=other)
                        r.save()
                    except:
                        print "route must be  unqiue"



        return HttpResponse("Routing Tools data saved successfully!!!")
