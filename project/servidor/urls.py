# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.servidor.views',  
    url(r'^$', 'inicio'),
    url(r'^consulta/', 'consulta'),
    url(r'^cadastro/', 'cadastro'),
    url(r'^edicao/(?P<id>\d+)/', 'edicao'),
    url(r'^relatorio/pdf/', 'relatorio_pdf'),
    url(r'^relatorio/ods/', 'relatorio_ods'),
    url(r'^relatorio/csv/', 'relatorio_csv'),
    url(r'^ferias/edicao/(?P<id>\d+)/', 'edicaoferias'),
    url(r'^ferias/cadastro/(?P<id>\d+)/', 'cadastroferias'),
    )