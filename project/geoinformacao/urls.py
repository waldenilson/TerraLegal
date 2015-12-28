# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.geoinformacao',
   url(r'^consulta', 'views.lista'),
   url(r'^terra_indigena', 'views.read_shp'),
   url(r'^importacao', 'views.importar_vw_parcelas'),
   url(r'^processo/processo_parcela_titulo/', 'processo.processo_parcela_titulo'),
    url(r'^parcela/consulta/', 'parcela.consulta'),
    url(r'^parcela/visualizacao/(?P<id>\d+)/', 'parcela.visualizacao'),
   )
