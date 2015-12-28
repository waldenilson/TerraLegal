# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.web',  
    url(r'^terra_legal/', 'views_publicas.terra_legal'),
    url(r'^equipe/', 'views_publicas.equipe'),
    url(r'^organizacao/', 'views_publicas.organizacao'),
    url(r'^mobile/', 'views_publicas.mobile'),
    url(r'^estatisticas/', 'estatisticas.estatisticas'),
    )



    