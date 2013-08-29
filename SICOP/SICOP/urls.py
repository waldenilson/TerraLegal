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
    url(r'^web/mda/', 'web.views_publicas.mda'),
    url(r'^web/processo_rural/', 'web.views_publicas.processo_rural'),
    url(r'^web/regularizacao_urbana/', 'web.views_publicas.regularizacao_urbana'),
    
    
    #INIT------------------------------SICOP---------------------------------------------------------------------------------
    
    # ACESSO RESTRITO SICOP PROCESSO
    url(r'^sicop/restrito/processo/consulta/', 'newsicop.restrito.processo.consulta'),
    url(r'^sicop/restrito/processo/cadastro/', 'newsicop.restrito.processo.cadastro'),
    url(r'^sicop/restrito/processo/edicao/', 'newsicop.restrito.processo.edicao'),
   
   # ACESSO RESTRITO SICOP PECA TECNICA 
    url(r'^sicop/restrito/peca_tecnica/consulta/', 'newsicop.restrito.peca_tecnica.consulta'),
    url(r'^sicop/restrito/peca_tecnica/cadastro/', 'newsicop.restrito.peca_tecnica.cadastro'),
    url(r'^sicop/restrito/peca_tecnica/edicao/(?P<id>\d+)/', 'newsicop.restrito.peca_tecnica.edicao'),
   
   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^sicop/restrito/contrato/consulta/', 'newsicop.restrito.contrato.consulta'),
    url(r'^sicop/restrito/contrato/cadastro/', 'newsicop.restrito.contrato.cadastro'),
    url(r'^sicop/restrito/contrato/edicao/(?P<id>\d+)/', 'newsicop.restrito.contrato.edicao'),
   
   # ACESSO RESTRITO SICOP CONJUGE
    url(r'^sicop/restrito/conjuge/consulta/', 'newsicop.restrito.conjuge.consulta'),
    url(r'^sicop/restrito/conjuge/cadastro/', 'newsicop.restrito.conjuge.cadastro'),
    url(r'^sicop/restrito/conjuge/edicao/(?P<id>\d+)/', 'newsicop.restrito.conjuge.edicao'),

    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/restrito/gleba/consulta/', 'newsicop.restrito.gleba.consulta'),
    url(r'^sicop/restrito/gleba/cadastro/', 'newsicop.restrito.gleba.cadastro'),
    url(r'^sicop/restrito/gleba/edicao/(?P<id>\d+)/', 'newsicop.restrito.gleba.edicao'),

    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/restrito/caixa/consulta/', 'newsicop.restrito.caixa.consulta'),
    url(r'^sicop/restrito/caixa/cadastro/', 'newsicop.restrito.caixa.cadastro'),
    url(r'^sicop/restrito/caixa/edicao/(?P<id>\d+)/', 'newsicop.restrito.caixa.edicao'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/restrito/sub_area/consulta/', 'newsicop.restrito.sub_area.consulta'),
    url(r'^sicop/restrito/sub_area/cadastro/', 'newsicop.restrito.sub_area.cadastro'),
    url(r'^sicop/restrito/sub_area/edicao/(?P<id>\d+)/', 'newsicop.restrito.sub_area.edicao'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/restrito/tipo_caixa/consulta/', 'newsicop.restrito.tipo_caixa.consulta'),
    url(r'^sicop/restrito/tipo_caixa/cadastro/', 'newsicop.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/restrito/tipo_caixa/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_caixa.edicao'),




    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/restrito/tipo_processo/consulta/', 'newsicop.restrito.tipo_processo.consulta'),
    url(r'^sicop/restrito/tipo_processo/cadastro/', 'newsicop.restrito.tipo_processo.cadastro'),
    url(r'^sicop/restrito/tipo_processo/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_processo.edicao'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/restrito/tipo_pendencia/consulta/', 'newsicop.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/restrito/tipo_pendencia/cadastro/', 'newsicop.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/restrito/tipo_pendencia/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_pendencia.edicao'),

    # ACESSO RESTRITO SICOP TIPO SITUACAO PROCESSO URBANO
    url(r'^sicop/restrito/tipo_situacao_processo_urbano/consulta/', 'newsicop.restrito.tipo_situacao_processo_urbano.consulta'),
    url(r'^sicop/restrito/tipo_situacao_processo_urbano/cadastro/', 'newsicop.restrito.tipo_situacao_processo_urbano.cadastro'),
    url(r'^sicop/restrito/tipo_situacao_processo_urbano/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_situacao_processo_urbano.edicao'),

    # ACESSO RESTRITO SICOP TIPO CLASSIFICACAO PROCESSO
    url(r'^sicop/restrito/tipo_classificacao_processo/consulta/', 'newsicop.restrito.tipo_classificacao_processo.consulta'),
    url(r'^sicop/restrito/tipo_classificacao_processo/cadastro/', 'newsicop.restrito.tipo_classificacao_processo.cadastro'),
    url(r'^sicop/restrito/tipo_classificacao_processo/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_classificacao_processo.edicao'),

    # ACESSO RESTRITO SICOP TIPO STATUS PENDENCIA
    url(r'^sicop/restrito/tipo_status_pendencia/consulta/', 'newsicop.restrito.tipo_status_pendencia.consulta'),
    url(r'^sicop/restrito/tipo_status_pendencia/cadastro/', 'newsicop.restrito.tipo_status_pendencia.cadastro'),
    url(r'^sicop/restrito/tipo_status_pendencia/edicao/(?P<id>\d+)/', 'newsicop.restrito.tipo_status_pendencia.edicao'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    url(r'^sicop/restrito/municipio/consulta/', 'newsicop.restrito.municipio.consulta'),
    url(r'^sicop/restrito/municipio/cadastro/', 'newsicop.restrito.municipio.cadastro'),
    url(r'^sicop/restrito/municipio/edicao/(?P<id>\d+)/', 'newsicop.restrito.municipio.edicao'),

    # ACESSO RESTRITO SICOP MUNICIPIO MODULO
    url(r'^sicop/restrito/municipio_modulo/consulta/', 'newsicop.restrito.municipio_modulo.consulta'),
    url(r'^sicop/restrito/municipio_modulo/cadastro/', 'newsicop.restrito.municipio_modulo.cadastro'),
    url(r'^sicop/restrito/municipio_modulo/edicao/(?P<id>\d+)/', 'newsicop.restrito.municipio_modulo.edicao'),


   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^sicop/restrito/relatorio/processo_peca', 'newsicop.restrito.relatorio.processo_peca'),
    url(r'^sicop/restrito/relatorio/peca_gleba', 'newsicop.restrito.relatorio.peca_gleba'),
    url(r'^sicop/restrito/relatorio/peca_nao_aprovada', 'newsicop.restrito.relatorio.peca_nao_aprovada'),
    url(r'^sicop/restrito/relatorio/peca_rejeitada', 'newsicop.restrito.relatorio.peca_rejeitada'),
    url(r'^sicop/restrito/relatorio/peca_sem_processo', 'newsicop.restrito.relatorio.peca_sem_processo'),
    url(r'^sicop/restrito/relatorio/peca_validada', 'newsicop.restrito.relatorio.peca_validada'),
    
    #END------------------------------SICOP---------------------------------------------------------------------------------
    
    
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"base/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
