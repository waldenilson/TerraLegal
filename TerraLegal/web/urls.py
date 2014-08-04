# coding: utf-8

from django.conf.urls import patterns, url

project = 'TerraLegal'
urlpatterns = patterns(project+'.web.views_publicas',  
    url(r'^terra_legal/', 'terra_legal'),
    url(r'^equipe/', 'equipe'),
    url(r'^organizacao/', 'organizacao'),
    
    )



    