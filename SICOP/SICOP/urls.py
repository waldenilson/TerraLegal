from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # ACESSO AO PUBLICO
    url(r'^$', 'web.views_publicas.inicio'),
    url(r'^web/terra_legal/', 'web.views_publicas.terra_legal'),
    url(r'^web/mda/', 'web.views_publicas.mda'),
    url(r'^web/processo_rural/', 'web.views_publicas.processo_rural'),
    url(r'^web/regularizacao_urbana/', 'web.views_publicas.regularizacao_urbana'),
    
    # ACESSO RESTRITO AO SICOP
    url(r'^sicop/acesso_restrito/', 'web.views.acesso_restrito'),
    
    # CONTROLE AUTENTICACAO
    url(r'^sicop/login/', 'django.contrib.auth.views.login', {"template_name":"sicop/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/sicop/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
)