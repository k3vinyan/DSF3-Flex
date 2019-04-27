# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from drivers.models import Driver
from routes.models import Block, Route
from jchart import Chart
from datetime import datetime, timedelta
from dsf3 import helpers
from collections import OrderedDict
# Create your views here.
def index(request):

    drivers = Driver.objects.filter(checkout=True)

    driversNameList = []
    driversTimeList = []
    for driver in drivers:
        checkout = driver.checkoutTime
        checkin = driver.checkinTime
        timeDiff = helpers.timeDifference(checkout, checkin)

        #convert to minutes
        t1 = sum(i*j for i, j in zip(map(int, str(timeDiff).split(':')), [60, 1, 1/60]))

        driversNameList.append(driver.firstName + " " + driver.lastName)
        driversTimeList.append(t1)


    #averageTime
    try:
        count = 0
        totalTime = 0
        for time in driversTimeList:
            count += 1
            totalTime += time
        average = "Approximately " + str(totalTime/count)
    except:
        average = "N/A"



    #chart
    class LineChart(Chart):
        chart_type = 'bar'
        options = {
            'maintainAspectRatio': True,
            'title': {
                'display': True,
                'text': 'Flex Checkin/Checkout Time',
                'fontSize': 36
            },
            'legend': {
                'display': True,
                'labels': {
                    'fontColor': 'rgb(255, 99, 132)'
                }
            }
        }
        def get_datasets(self, **kwargs):

            return [{
                'label': "Time (minutes)",
                'data': driversTimeList
            }]
        def get_labels(self, **kwargs):
            return driversNameList

    drivers = Driver.objects.all()
    blocks = Block.objects.order_by('startTime').all()


    unplannedData = OrderedDict()

    for block in blocks:
        unplannedData[block] = {
            'accepted': 0,
            'actual': 0,
            'unplanned': 0,
            'bridge': []
        }

    for driver in drivers:
        unplannedData[driver.block]['accepted'] += 1
        if driver.isAssigned == True:
            if driver.route.isSplit == True or driver.route.isUnplanned == True:
                unplannedData[driver.block]['unplanned'] += 1
                unplannedData[driver.block]['bridge'].append(driver.route.route + ", ")
            else:
                unplannedData[driver.block]['actual'] += 1

    return  render(request, 'summary/index.html', {
        'line_chart': LineChart(),
        'unplannedData': unplannedData,
        'averageTime': average
    })
