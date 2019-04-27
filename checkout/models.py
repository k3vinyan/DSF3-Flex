# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from routes.models import Route

# Create your models here.
class RoutingtoolsRoute(models.Model):
     route       = models.CharField(max_length=10, null=True, unique=True)
     cluster     = models.CharField(max_length=10, blank=True)
     atStation   = models.CharField(max_length=10, blank=True)
     delivered   = models.CharField(max_length=10, blank=True)
     attempted   = models.CharField(max_length=10, blank=True)
     departure   = models.CharField(max_length=10, blank=True)
     betweenFC   = models.CharField(max_length=10, blank=True)
     undelivered = models.CharField(max_length=10, blank=True)
     other       = models.CharField(max_length=10, blank=True)
     onRoad      = models.CharField(max_length=10, blank=True)
