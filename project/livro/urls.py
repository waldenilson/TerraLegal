# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.livro',  
    url(r'^consulta/', 'views.consulta'),
    url(r'^cadastro/', 'views.cadastro'),
    url(r'^edicao/(?P<id>\d+)/', 'views.edicao'),
    url(r'^titulos_entregues/','views.titulos_entregues'),
    url(r'^titulos_nao_entregues/','views.titulos_nao_entregues'),
    url(r'^relatorio/ods', 'views.relatorio_ods'),
    url(r'^status_titulo/consulta/', 'status_titulo.consulta'),
    url(r'^status_titulo/cadastro/', 'status_titulo.cadastro'),
    url(r'^status_titulo/edicao/(?P<id>\d+)/', 'status_titulo.edicao'),

)
