# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.core',

    url(r'^excecao/500/', 'views_excecoes.erro_servidor'),
    url(r'^excecao/404/', 'views_excecoes.pagina_nao_encontrada'),
    url(r'^excecao/403/', 'views_excecoes.permissao_negada'),

   )
   
