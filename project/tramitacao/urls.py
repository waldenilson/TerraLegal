# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.tramitacao',

   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^contrato/consulta/', 'restrito.contrato.consulta'),
    url(r'^contrato/cadastro/', 'restrito.contrato.cadastro'),
    url(r'^contrato/edicao/(?P<id>\d+)/', 'restrito.contrato.edicao'),

   )
