# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#from django_mysql.models import Model, ListCharField

# Create your models here.
class Route(models.Model):
     route          = models.CharField(max_length=10)
     cluster        = models.CharField(max_length=10)
     isAssigned     = models.BooleanField(default=False)
     tbaCount       = models.CharField(max_length=50, blank=True)
     DP             = models.CharField(max_length=50, blank=True, null=True)
     isSplit        = models.BooleanField(default=False)
     isUnplanned    = models.BooleanField(default=False)
     isAssignedTime = models.CharField(max_length=10, null=True, default=None)

     # def __str__(self):
     #     return self.route

     class Meta:
         ordering = ('cluster', 'route',)



class Block(models.Model):
    date        = models.DateTimeField(max_length=15, blank=True, null=True)
    startTime   = models.CharField(max_length=10)
    endTime     = models.CharField(max_length=10)
    shiftLength = models.CharField(max_length=10)
    create_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.startTime + " - " + self.endTime

class Tba(models.Model):
    driver      = models.ForeignKey('drivers.Driver', blank=True, null=True)
    route       = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    tba         = models.CharField(max_length=20)
    status      = models.CharField(max_length=20)
    link        = models.CharField(max_length=30)
    address     = models.CharField(max_length=20)
    city        = models.CharField(max_length=15, blank=True)
    sortZone    = models.CharField(max_length=10, blank=True)
    zipCode     = models.CharField(max_length=15, blank=True)

    # def __str__(self):
    #     return self.tba
