# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.calculo.views',
   url(r'^portaria23', 'consulta'),
   url(r'^emissao/(?P<id>\d+)/', 'emissao'),
   url(r'^processo/digitar/', 'digitar'),
   url(r'^geraPDF/', 'geraPDF'),
   url(r'^geraGRU/(?P<id>\d+)/', 'geraGRU'),


   )