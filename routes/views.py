# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from routes.models import Tba, Route
from dsf3 import helpers
from django.core.exceptions import ObjectDoesNotExist
import json
import requests

# Create your views here.
def index(request):
    #get request
    if request.method == 'GET':

        #sort route with tbas
        allTbas = Tba.objects.all()
        allRoutes = Route.objects.all()

        clusterCount = {}
        routeCount = {}

        for route in allRoutes:
            if route.cluster not in clusterCount:
                clusterCount[route.cluster] = 1
            else:
                clusterCount[route.cluster] += 1

        for tba in allTbas:
            if tba.route not in routeCount:
                routeCount[tba.route] = 1
            else:
                routeCount[tba.route] += 1

        for route, count in routeCount.items():
            if route.isSplit == False and route.isUnplanned == False:
                r = Route.objects.get(route=route.route)
                r.tbaCount = count
                r.save(update_fields=['tbaCount'])

        return render(request, 'routes/index.html', {'clusterCount': clusterCount, 'routeCount':routeCount, 'allTbas': allTbas, 'allRoutes': allRoutes})
    
    #post request
    if request.method == 'POST':
        
        tbas =  request.POST.get('tbas')

        existArray = []
        noRouteArray = []
       
        for item in data:
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
                status = item['status']
                link = item['link']
                address = item['address']
                tba = Tba(route=r, tba=tba, status=status, link=link, address=address)
                tba.save()


            else:
                tbaTotal += 1
                existArray.append(tba.tba)
        existArrayLength = len(existArray)
        allRoutes = Route.objects.all()

        message = {'tbaCount': tbaCount, 'tbaTotal': tbaTotal, 'existArray': existArray, 'existArrayLength': existArrayLength, 'routeCount': routeCount}
        return render(request, 'routes/index.html', {'message': message, 'allRoutes': allRoutes})


def addRoute(request):

    if request.method == "POST":
        type = request.POST.get('type')
        route = request.POST.get('route')
        quantity = request.POST.get('quantity')
        tbas = request.POST.get('tbas')
        tbasList = tbas.split("\n")

        if type == "Split":
            routeValue = route + "-" + type
            route = Route(route=routeValue, tbaCount=quantity, isSplit=True, cluster=routeValue)
            route.save()
        else:
            routeValue = type + "-" + route
            route = Route(route=routeValue, tbaCount=quantity, isUnplanned=True, cluster=type)
            route.save()

        for tba in tbasList:
            try:
                tba = Tba.objects.get(tba=tba).update(route=addRoute)
                tba.route = addRoute
                if type == "Split":
                    tba.update(isSplit=True)
                else:
                    tba.update(isUnplanned=True)
                tba.save()
            except:
                if type == "Split":
                    newTba = Tba(tba=tba, route=route)
                    newTba.save()
                else:
                    newTba = Tba(tba=tba, route=route)
                    newTba.save()

        message = "Route Addded Successfully!"
        return render(request, 'routes/index.html', {'message': message})
        #return redirect('/routes')

def deleteRoute(request):

    if request.method == "POST":
        route = request.POST.get('route')
        Route.objects.filter(route=route).delete()
        return redirect('/routes')
