
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_config
admin.autodiscover()

urlpatterns = patterns('',
    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # ACESSO AO PUBLICO
    url(r'^$', 'web.views_publicas.inicio'),
    url(r'^web/terra_legal/', 'web.views_publicas.terra_legal'),
    url(r'^web/mda/', 'web.views_publicas.mda'),
    url(r'^web/processo_rural/', 'web.views_publicas.processo_rural'),
    url(r'^web/regularizacao_urbana/', 'web.views_publicas.regularizacao_urbana'),
    
    # ACESSO RESTRITO AO SICOP
    url(r'^sicop/acesso_restrito/', 'web.views.acesso_restrito'),
    url(r'^sicop/processos/', 'web.views.processos'),
    url(r'^sicop/processos_novo/', 'web.views.processos_novo'),
    url(r'^sicop/processos_edicao/', 'web.views.processos_edicao'),
   
    url(r'^sicop/pecas_tecnicas/', 'web.views.pecas_tecnicas'),
    url(r'^sicop/pecas_tecnicas_novo/', 'web.views.pecas_tecnicas_novo'),
    url(r'^sicop/pecas_tecnicas_edicao/', 'web.views.pecas_tecnicas_edicao'),
   
    url(r'^sicop/relatorios/', 'web.views.relatorios'),
    
    # CONTROLE AUTENTICACAO
    url(r'^sicop/login/', 'django.contrib.auth.views.login', {"template_name":"sicop/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/sicop/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
)