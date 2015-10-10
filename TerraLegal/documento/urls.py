# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.documento',

    url(r'^memorando/consulta/', 'memorando.consulta'),   
    url(r'^memorando/cadastro/', 'memorando.cadastro'),   
    url(r'^memorando/edicao/(?P<id>\d+)/', 'memorando.edicao'),   

   )
   
