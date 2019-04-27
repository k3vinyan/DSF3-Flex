# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from routes.models import Route, Block
# Create your models here.
class Driver(models.Model):
    DPID            = models.CharField(max_length=20, default=False)
    fullName        = models.CharField(max_length=30, blank=True)
    firstName       = models.CharField(max_length=15, blank=True)
    lastName        = models.CharField(max_length=15, blank=True)
    checkin         = models.BooleanField(default=False)
    isAssigned      = models.BooleanField(default=False)
    shiftLength     = models.CharField(max_length=20, blank=True)
    startTime       = models.CharField(max_length=10, blank=True)
    endTime         = models.CharField(max_length=10, blank=True)
    isNoShow        = models.BooleanField(default=False)
    checkout        = models.BooleanField(default=False)
    packageScan     = models.CharField(max_length=3, blank=True)
    routingTool     = models.CharField(max_length=3, blank=True)
    route           = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, default=None)
    block           = models.ForeignKey(Block, null=True)
    checkinTime     = models.CharField(max_length=15, null=True, default=None)
    checkoutTime    = models.CharField(max_length=15, null=True, default=None)


    def __str__(self):
        return self.firstName + " " + self.lastName

    class Meta:
        ordering = ('block', 'firstName',)
