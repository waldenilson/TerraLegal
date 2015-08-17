# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.geoinformacao',
   url(r'^consulta', 'views.consulta'),
   url(r'^processo/consulta/', 'processo.consulta'),
   )
