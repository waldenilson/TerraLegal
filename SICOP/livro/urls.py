# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('livro.views',  
    url(r'^consulta/', 'consulta'),
    url(r'^cadastro/', 'cadastro'),
    url(r'^edicao/(?P<id>\d+)/', 'edicao'),
    url(r'^titulos_entregues/','titulos_entregues'),
    url(r'^titulos_nao_entregues/','titulos_nao_entregues'),
    url(r'^relatorio/ods', 'relatorio_ods'),
    
    )