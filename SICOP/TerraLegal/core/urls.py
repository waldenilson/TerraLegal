# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.core.views_excecoes',

    url(r'^500/', 'erro_servidor'),
    url(r'^404/', 'pagina_nao_encontrada'),
    url(r'^403/', 'permissao_negada'),

   )
   
