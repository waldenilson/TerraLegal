# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.calculo',
   url(r'^portaria23', 'views.consulta'),
   url(r'^emissao/(?P<id>\d+)/', 'views.emissao'),
   url(r'^processo/digitar/', 'views.digitar'),
   url(r'^geraPDF/', 'views.geraPDF'),
   url(r'^geraGRU/(?P<id>\d+)/', 'views.geraGRU'),

   url(r'^tr_mensal/consulta/', 'tr_mensal.consulta'),
   url(r'^tr_mensal/cadastro/', 'tr_mensal.cadastro'),
   url(r'^tr_mensal/edicao/(?P<id>\d+)/', 'tr_mensal.edicao'),

   )
