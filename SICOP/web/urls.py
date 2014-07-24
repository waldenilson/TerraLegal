# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('web.views_publicas',  
    url(r'^terra_legal/', 'terra_legal'),
    url(r'^equipe/', 'equipe'),
    url(r'^processo_rural/', 'processo_rural'),
    url(r'^regularizacao_urbana/', 'regularizacao_urbana'),
    url(r'^organizacao/', 'organizacao'),
    
    )



    