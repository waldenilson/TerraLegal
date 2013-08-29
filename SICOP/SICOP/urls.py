#teste commit eduardo 20130828
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_config
from dajaxice.core.Dajaxice import dajaxice_autodiscover
admin.autodiscover()

handler404 = 'web.views_excecoes.pagina_nao_encontrada'
handler403 = 'web.views_excecoes.permissao_negada'
handler500 = 'web.views_excecoes.erro_servidor'

urlpatterns = patterns('',
    
    # DAJAXICE AJAX DO PROJETO
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    
    # ACESSO AO PUBLICO
    url(r'^$', 'web.views_publicas.inicio'),
    url(r'^web/terra_legal/', 'web.views_publicas.terra_legal'),
    url(r'^web/relatorio/', 'web.views_publicas.relatorio'),
    url(r'^web/mda/', 'web.views_publicas.mda'),
    url(r'^web/processo_rural/', 'web.views_publicas.processo_rural'),
    url(r'^web/regularizacao_urbana/', 'web.views_publicas.regularizacao_urbana'),
    
    # ACESSO RESTRITO AO SICOP
    url(r'^sicop/restrito/processo/consulta/', 'web.sicop.restrito.processo.consulta'),
    url(r'^sicop/restrito/processo/cadastro/', 'web.sicop.restrito.processo.cadastro'),
    url(r'^sicop/restrito/processo/edicao/', 'web.sicop.restrito.processo.edicao'),
   
    url(r'^sicop/restrito/peca_tecnica/consulta/', 'web.sicop.restrito.peca_tecnica.consulta'),
    url(r'^sicop/restrito/peca_tecnica/cadastro/', 'web.sicop.restrito.peca_tecnica.cadastro'),
    url(r'^sicop/restrito/peca_tecnica/edicao/(?P<id_peca>\d+)/', 'web.sicop.restrito.peca_tecnica.edicao'),
   
    url(r'^sicop/relatorios/', 'web.views.relatorios'),
    
    # CONTROLE AUTENTICACAO
    url(r'^sicop/login/', 'django.contrib.auth.views.login', {"template_name":"sicop/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/sicop/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
