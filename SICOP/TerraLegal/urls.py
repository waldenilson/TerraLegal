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
    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^sicop/restrito/processo/consulta/', 'sicop.restrito.processo.consulta'),
    url(r'^sicop/restrito/processo/cadastro/', 'sicop.restrito.processo.cadastro'),
    # PROCESSO RURAL
    url(r'^sicop/restrito/processo/rural/consulta/', 'sicop.restrito.processo_rural.consulta'),
    url(r'^sicop/restrito/processo/rural/cadastro/', 'sicop.restrito.processo_rural.cadastro'),
    url(r'^sicop/restrito/processo/rural/edicao/(?P<id>\d+)/', 'sicop.restrito.processo_rural.edicao'),
    # PROCESSO URBANO
    url(r'^sicop/restrito/processo/urbano/consulta/', 'sicop.restrito.processo_urbano.consulta'),
    url(r'^sicop/restrito/processo/urbano/cadastro/', 'sicop.restrito.processo_urbano.cadastro'),
    url(r'^sicop/restrito/processo/urbano/edicao/(?P<id>\d+)/', 'sicop.restrito.processo_urbano.edicao'),
    # PROCESSO CLAUSULA RESOLUTIVA
    url(r'^sicop/restrito/processo/clausula/consulta/', 'sicop.restrito.processo_clausula.consulta'),
    url(r'^sicop/restrito/processo/clausula/cadastro/', 'sicop.restrito.processo_clausula.cadastro'),
    url(r'^sicop/restrito/processo/clausula/edicao/(?P<id>\d+)/', 'sicop.restrito.processo_clausula.edicao'),
   
    
   # ACESSO RESTRITO SICOP PECA TECNICA 
    url(r'^sicop/restrito/peca_tecnica/consulta/', 'sicop.restrito.peca_tecnica.consulta'),
    url(r'^sicop/restrito/peca_tecnica/cadastro/', 'sicop.restrito.peca_tecnica.cadastro'),
    url(r'^sicop/restrito/peca_tecnica/edicao/(?P<id>\d+)/', 'sicop.restrito.peca_tecnica.edicao'),
   
   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^sicop/restrito/contrato/consulta/', 'sicop.restrito.contrato.consulta'),
    url(r'^sicop/restrito/contrato/cadastro/', 'sicop.restrito.contrato.cadastro'),
    url(r'^sicop/restrito/contrato/edicao/(?P<id>\d+)/', 'sicop.restrito.contrato.edicao'),
   
   # ACESSO RESTRITO SICOP CONJUGE
    url(r'^sicop/restrito/conjuge/consulta/', 'sicop.restrito.conjuge.consulta'),
    url(r'^sicop/restrito/conjuge/cadastro/', 'sicop.restrito.conjuge.cadastro'),
    url(r'^sicop/restrito/conjuge/edicao/(?P<id>\d+)/', 'sicop.restrito.conjuge.edicao'),

    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/restrito/gleba/consulta/', 'sicop.restrito.gleba.consulta'),
    url(r'^sicop/restrito/gleba/cadastro/', 'sicop.restrito.gleba.cadastro'),
    url(r'^sicop/restrito/gleba/edicao/(?P<id>\d+)/', 'sicop.restrito.gleba.edicao'),

    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/restrito/caixa/consulta/', 'sicop.restrito.caixa.consulta'),
    url(r'^sicop/restrito/caixa/cadastro/', 'sicop.restrito.caixa.cadastro'),
    url(r'^sicop/restrito/caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.caixa.edicao'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/restrito/sub_area/consulta/', 'sicop.restrito.sub_area.consulta'),
    url(r'^sicop/restrito/sub_area/cadastro/', 'sicop.restrito.sub_area.cadastro'),
    url(r'^sicop/restrito/sub_area/edicao/(?P<id>\d+)/', 'sicop.restrito.sub_area.edicao'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/restrito/tipo_caixa/consulta/', 'sicop.restrito.tipo_caixa.consulta'),
    url(r'^sicop/restrito/tipo_caixa/cadastro/', 'sicop.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/restrito/tipo_caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_caixa.edicao'),




    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/restrito/tipo_processo/consulta/', 'sicop.restrito.tipo_processo.consulta'),
    url(r'^sicop/restrito/tipo_processo/cadastro/', 'sicop.restrito.tipo_processo.cadastro'),
    url(r'^sicop/restrito/tipo_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_processo.edicao'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/restrito/tipo_pendencia/consulta/', 'sicop.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/restrito/tipo_pendencia/cadastro/', 'sicop.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/restrito/tipo_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_pendencia.edicao'),

    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^sicop/restrito/situacao_processo/consulta/', 'sicop.restrito.situacao_processo.consulta'),
    url(r'^sicop/restrito/situacao_processo/cadastro/', 'sicop.restrito.situacao_processo.cadastro'),
    url(r'^sicop/restrito/situacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_processo.edicao'),

    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^sicop/restrito/situacao_geo/consulta/', 'sicop.restrito.situacao_geo.consulta'),
    url(r'^sicop/restrito/situacao_geo/cadastro/', 'sicop.restrito.situacao_geo.cadastro'),
    url(r'^sicop/restrito/situacao_geo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_geo.edicao'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^sicop/restrito/classificacao_processo/consulta/', 'sicop.restrito.classificacao_processo.consulta'),
    url(r'^sicop/restrito/classificacao_processo/cadastro/', 'sicop.restrito.classificacao_processo.cadastro'),
    url(r'^sicop/restrito/classificacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.classificacao_processo.edicao'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^sicop/restrito/status_pendencia/consulta/', 'sicop.restrito.status_pendencia.consulta'),
    url(r'^sicop/restrito/status_pendencia/cadastro/', 'sicop.restrito.status_pendencia.cadastro'),
    url(r'^sicop/restrito/status_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.status_pendencia.edicao'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    url(r'^sicop/restrito/municipio/consulta/', 'sicop.restrito.municipio.consulta'),
    url(r'^sicop/restrito/municipio/cadastro/', 'sicop.restrito.municipio.cadastro'),
    url(r'^sicop/restrito/municipio/edicao/(?P<id>\d+)/', 'sicop.restrito.municipio.edicao'),

    # ACESSO RESTRITO SICOP MUNICIPIO MODULO
    url(r'^sicop/restrito/municipio_modulo/consulta/', 'sicop.restrito.municipio_modulo.consulta'),
    url(r'^sicop/restrito/municipio_modulo/cadastro/', 'sicop.restrito.municipio_modulo.cadastro'),
    url(r'^sicop/restrito/municipio_modulo/edicao/(?P<id>\d+)/', 'sicop.restrito.municipio_modulo.edicao'),


   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^sicop/restrito/relatorio/processo_peca', 'sicop.restrito.relatorio.processo_peca'),
    url(r'^sicop/restrito/relatorio/peca_gleba', 'sicop.restrito.relatorio.peca_gleba'),
    url(r'^sicop/restrito/relatorio/peca_nao_aprovada', 'sicop.restrito.relatorio.peca_nao_aprovada'),
    url(r'^sicop/restrito/relatorio/peca_rejeitada', 'sicop.restrito.relatorio.peca_rejeitada'),
    url(r'^sicop/restrito/relatorio/peca_sem_processo', 'sicop.restrito.relatorio.peca_sem_processo'),
    url(r'^sicop/restrito/relatorio/peca_validada', 'sicop.restrito.relatorio.peca_validada'),
    
    #END------------------------------SICOP---------------------------------------------------------------------------------
    
    #INIT------------------------------CONTROLE---------------------------------------------------------------------------------
    # ACESSO SISTEMAS DE CONTROLE
    url(r'^controle/', 'controle.views.inicio'),
    url(r'^controle/restrito/servidor', 'servidor.restrito.consulta'),
    
    #END------------------------------CONTROLE---------------------------------------------------------------------------------
    
    
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"base/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
