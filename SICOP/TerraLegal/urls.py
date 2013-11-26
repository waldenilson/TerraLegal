#teste commit eduardo 20130828
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_config
from dajaxice.core.Dajaxice import dajaxice_autodiscover
from TerraLegal import settings
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
    
    # PERMISSAO NEGADA
    url(r'^excecoes/permissao_negada/', 'web.views_excecoes.permissao_negada'),   
    
    # ACESSO RESTRITO SICOP PROCESSO
    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^sicop/restrito/processo/consulta/', 'sicop.restrito.processo.consulta'),   
    url(r'^sicop/restrito/processo/cadastro/', 'sicop.restrito.processo.cadastro'),
    url(r'^sicop/restrito/processo/edicao/(?P<id>\d+)/', 'sicop.restrito.processo.edicao'),
    url(r'^sicop/restrito/processo/tramitacao/(?P<base>\d+)/', 'sicop.restrito.processo.tramitar'),
    url(r'^sicop/restrito/processo/anexo/(?P<base>\d+)/', 'sicop.restrito.processo.anexar'),
    url(r'^sicop/restrito/processo/pendencia/(?P<base>\d+)/', 'sicop.restrito.processo.criar_pendencia'),   
    url(r'^sicop/restrito/processo/relatorio/', 'sicop.restrito.processo.relatorio'),

    # ACESSO RESTRITO SICOP PENDENCIA
    url(r'^sicop/restrito/pendencia/edicao/(?P<pendencia>\d+)/', 'sicop.restrito.pendencia.edicao'),
    
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
     url(r'^sicop/restrito/peca_tecnica/relatorio/', 'sicop.restrito.peca_tecnica.relatorio'),
  
   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^sicop/restrito/contrato/consulta/', 'sicop.restrito.contrato.consulta'),
    url(r'^sicop/restrito/contrato/cadastro/', 'sicop.restrito.contrato.cadastro'),
    url(r'^sicop/restrito/contrato/edicao/(?P<id>\d+)/', 'sicop.restrito.contrato.edicao'),
    url(r'^sicop/restrito/contrato/relatorio/', 'sicop.restrito.contrato.relatorio'),    
  
   # ACESSO RESTRITO SICOP PREGAO 
    url(r'^sicop/restrito/pregao/consulta/', 'sicop.restrito.pregao.consulta'),
    url(r'^sicop/restrito/pregao/cadastro/', 'sicop.restrito.pregao.cadastro'),
    url(r'^sicop/restrito/pregao/edicao/(?P<id>\d+)/', 'sicop.restrito.pregao.edicao'),
    url(r'^sicop/restrito/pregao/relatorio/', 'sicop.restrito.pregao.relatorio'),    

    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/restrito/gleba/consulta/', 'sicop.restrito.gleba.consulta'),
    url(r'^sicop/restrito/gleba/cadastro/', 'sicop.restrito.gleba.cadastro'),
    url(r'^sicop/restrito/gleba/edicao/(?P<id>\d+)/', 'sicop.restrito.gleba.edicao'),
    url(r'^sicop/restrito/gleba/relatorio/', 'sicop.restrito.gleba.relatorio'),

    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/restrito/caixa/consulta/', 'sicop.restrito.caixa.consulta'),
    url(r'^sicop/restrito/caixa/cadastro/', 'sicop.restrito.caixa.cadastro'),
    url(r'^sicop/restrito/caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.caixa.edicao'),
    url(r'^sicop/restrito/caixa/relatorio/', 'sicop.restrito.caixa.relatorio'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/restrito/sub_area/consulta/', 'sicop.restrito.sub_area.consulta'),
    url(r'^sicop/restrito/sub_area/cadastro/', 'sicop.restrito.sub_area.cadastro'),
    url(r'^sicop/restrito/sub_area/edicao/(?P<id>\d+)/', 'sicop.restrito.sub_area.edicao'),
    url(r'^sicop/restrito/sub_area/relatorio/', 'sicop.restrito.sub_area.relatorio'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/restrito/tipo_caixa/consulta/', 'sicop.restrito.tipo_caixa.consulta'),
    url(r'^sicop/restrito/tipo_caixa/cadastro/', 'sicop.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/restrito/tipo_caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_caixa.edicao'),
    url(r'^sicop/restrito/tipo_caixa/relatorio/', 'sicop.restrito.tipo_caixa.relatorio'),


    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/restrito/tipo_processo/consulta/', 'sicop.restrito.tipo_processo.consulta'),
    url(r'^sicop/restrito/tipo_processo/cadastro/', 'sicop.restrito.tipo_processo.cadastro'),
    url(r'^sicop/restrito/tipo_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_processo.edicao'),
    url(r'^sicop/restrito/tipo_processo/relatorio/', 'sicop.restrito.tipo_processo.relatorio'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/restrito/tipo_pendencia/consulta/', 'sicop.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/restrito/tipo_pendencia/cadastro/', 'sicop.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/restrito/tipo_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_pendencia.edicao'),
    url(r'^sicop/restrito/tipo_pendencia/relatorio/', 'sicop.restrito.tipo_pendencia.relatorio'),

    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^sicop/restrito/situacao_processo/consulta/', 'sicop.restrito.situacao_processo.consulta'),
    url(r'^sicop/restrito/situacao_processo/cadastro/', 'sicop.restrito.situacao_processo.cadastro'),
    url(r'^sicop/restrito/situacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_processo.edicao'),
    url(r'^sicop/restrito/situacao_processo/relatorio/', 'sicop.restrito.situacao_processo.relatorio'),

    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^sicop/restrito/situacao_geo/consulta/', 'sicop.restrito.situacao_geo.consulta'),
    url(r'^sicop/restrito/situacao_geo/cadastro/', 'sicop.restrito.situacao_geo.cadastro'),
    url(r'^sicop/restrito/situacao_geo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_geo.edicao'),
    url(r'^sicop/restrito/situacao_geo/relatorio/', 'sicop.restrito.situacao_geo.relatorio'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^sicop/restrito/classificacao_processo/consulta/', 'sicop.restrito.classificacao_processo.consulta'),
    url(r'^sicop/restrito/classificacao_processo/cadastro/', 'sicop.restrito.classificacao_processo.cadastro'),
    url(r'^sicop/restrito/classificacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.classificacao_processo.edicao'),
    url(r'^sicop/restrito/classificacao_processo/relatorio/', 'sicop.restrito.classificacao_processo.relatorio'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^sicop/restrito/status_pendencia/consulta/', 'sicop.restrito.status_pendencia.consulta'),
    url(r'^sicop/restrito/status_pendencia/cadastro/', 'sicop.restrito.status_pendencia.cadastro'),
    url(r'^sicop/restrito/status_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.status_pendencia.edicao'),
    url(r'^sicop/restrito/status_pendencia/relatorio/', 'sicop.restrito.status_pendencia.relatorio'),

   # ACESSO RESTRITO SICOP DIVISAO
    url(r'^sicop/restrito/divisao/consulta/', 'sicop.restrito.divisao.consulta'),
    url(r'^sicop/restrito/divisao/cadastro/', 'sicop.restrito.divisao.cadastro'),
    url(r'^sicop/restrito/divisao/edicao/(?P<id>\d+)/', 'sicop.restrito.divisao.edicao'),
    url(r'^sicop/restrito/divisao/relatorio/', 'sicop.restrito.divisao.relatorio'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^sicop/restrito/grupo/consulta/', 'sicop.restrito.grupo.consulta'),
    url(r'^sicop/restrito/grupo/cadastro/', 'sicop.restrito.grupo.cadastro'),
    url(r'^sicop/restrito/grupo/edicao/(?P<id>\d+)/', 'sicop.restrito.grupo.edicao'),
    url(r'^sicop/restrito/grupo/relatorio/', 'sicop.restrito.grupo.relatorio'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^sicop/restrito/usuario/consulta/', 'sicop.restrito.usuario.consulta'),
    url(r'^sicop/restrito/usuario/cadastro/', 'sicop.restrito.usuario.cadastro'),
    url(r'^sicop/restrito/usuario/edicao/(?P<id>\d+)/', 'sicop.restrito.usuario.edicao'),
    url(r'^sicop/restrito/usuario/edicao/usuario/(?P<id>\d+)/', 'sicop.restrito.usuario.edicao_usuario_logado'),
    url(r'^sicop/restrito/usuario/relatorio/', 'sicop.restrito.usuario.relatorio'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    url(r'^sicop/restrito/municipio/consulta/', 'sicop.restrito.municipio.consulta'),
    url(r'^sicop/restrito/municipio/cadastro/', 'sicop.restrito.municipio.cadastro'),
    url(r'^sicop/restrito/municipio/edicao/(?P<id>\d+)/', 'sicop.restrito.municipio.edicao'),
   
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
    url(r'^controle/$', 'controle.views.inicio'),
    url(r'^controle/restrito/servidor/consulta/', 'servidor.restrito.servidor.consulta'),
    url(r'^controle/restrito/servidor/cadastro/', 'servidor.restrito.servidor.cadastro'),
    url(r'^controle/restrito/servidor/edicao/(?P<id>\d+)/', 'servidor.restrito.servidor.edicao'),
    url(r'^controle/restrito/servidor/relatorio/', 'servidor.restrito.servidor.relatorio'),
   
    
    #END------------------------------CONTROLE---------------------------------------------------------------------------------
    
    
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"base/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/login/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
