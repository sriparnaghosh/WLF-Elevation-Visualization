# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models


# Create your models here.
class Position(models.Model):
    lat = models.IntegerField()
    long = models.IntegerField()
