# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('calculo.views',
   url(r'^portaria23', 'consulta'),
   url(r'^processo/(?P<id>\d+)/', 'emissao'),
   )