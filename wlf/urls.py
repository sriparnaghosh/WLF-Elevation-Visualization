from django.conf.urls import url
from . import views
from django.contrib import admin
app_name= 'wlf'
url(r'^$',views.base,name='base')