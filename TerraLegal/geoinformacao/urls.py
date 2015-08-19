# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.geoinformacao',
   url(r'^consulta', 'views.lista'),
   url(r'^processo/processo_parcela_titulo/', 'processo.processo_parcela_titulo'),
   )
