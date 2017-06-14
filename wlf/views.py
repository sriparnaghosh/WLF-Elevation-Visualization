# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson
import urllib

from django.shortcuts import render

# Create your views here.
from wlf.models import Position

lat_list = Position.objects.all().values_list('lat')
long_list = Position.objects.all().values_list('long')

xmin = min(lat_list)
xmax = max(lat_list)
ymin = min(long_list)
ymax = max(long_list)

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json?locations='

# computing elevations of all coordinates
elevation_matrix = [[]]
index_i = 0
index_j = 0
elevation_sum = 0 n= 0
count = [[]]
for i in range(xmin, xmax):
    for j in range(ymax, ymin, -1):
        n = n + 1
        url = ELEVATION_BASE_URL + i + "," + j + "&key=AIzaSyAJYe1NaEaTtRRrKZvGr1sa35druR5TkbA"
        response = simplejson.load(urllib.urlopen(url))
        elevation_matrix[index_i][index_j] = response['results']['elevation']
        elevation_sum += elevation_matrix[index_i][index_j]
        count[index_i][index_j] = 0
        index_j += 1
    index_i += 1

# normalizing the elevation matrix
for i in range(xmin, xmax):
    for j in range(ymax, ymin, -1):
        elevation_matrix[i][j] = elevation_matrix[i][j] / elevation_sum
pos = [[]]
for i in range(0, n, 1):
    maxx = 0
    for j in range(xmin, xmax):
        for k in range(ymax, ymin, -1):
            if max(elevation_matrix) > maxx:
                maxx = max(elevation_matrix)
                posx = j
                posy = k

    if (maxx > -1):

        if (posx > 0) and (elevation_matrix[posx][posy] != -1):
            count[posx - 1][posy] = count[posx][posy] + 1
        if (posx < index_i) and (elevation_matrix[posx][posy] != -1):
            count[posx + 1][posy] = count[posx][posy] + 1
        if (posy > 0) and (elevation_matrix[posx][posy] != -1):
            count[posx][posy - 1] = count[posx][posy] + 1
        if (posx < index_i) and (elevation_matrix[posx][posy] != -1):
            count[posx][posy + 1] = count[posx][posy] + 1
    elevation_matrix[posx][posy] = -1
