# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.documento',

    url(r'^memorando/consulta/', 'memorando.consulta'),   
    url(r'^memorando/cadastro/', 'memorando.cadastro'),   
    url(r'^memorando/edicao/(?P<id>\d+)/', 'memorando.edicao'),   

    url(r'^oficio/consulta/', 'oficio.consulta'),   
    url(r'^oficio/cadastro/', 'oficio.cadastro'),   
    url(r'^oficio/edicao/(?P<id>\d+)/', 'oficio.edicao'),   

    url(r'^lista/', 'views.lista'),

   )
   
