# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
from dsf3 import helpers
from bs4 import BeautifulSoup
from routes.models import Block, Route
from drivers.models import Driver
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):

    if request.method == 'GET':

        #this is seed data

        blocks = Block.objects.order_by('startTime').all()
        drivers = Driver.objects.order_by('startTime', 'firstName').all()

        driversData = {}

        for driver in drivers:
            for block in blocks:
                if block.startTime == driver.startTime:
                        try:
                            driversData[block.startTime]
                        except KeyError:
                            driversData[block.startTime] = {
                                'accepted': 0,
                                'showed': 0,
                                'noShow': 0,
                            }
                        driversData[block.startTime]['accepted'] += 1

                        if driver.checkout == True:
                            driversData[block.startTime]['showed'] += 1
                        if driver.isNoShow == True:
                            driversData[block.startTime]['noShow'] += 1

        return render(request, 'drivers/index.html', {'drivers':drivers, 'blocks':blocks, 'driversData':driversData})


#for development only, tests
def roster(request):
    return render(request, 'drivers/test-roster.html')
