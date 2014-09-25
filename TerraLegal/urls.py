# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()

project = 'TerraLegal'

handler404 = project+'.core.views_excecoes.pagina_nao_encontrada'
handler403 = project+'.core.views_excecoes.permissao_negada'
handler500 = project+'.core.views_excecoes.erro_servidor'

urlpatterns = patterns('',
    
    # DAJAXICE AJAX DO PROJETO
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^livro/',include(project+'.livro.urls',namespace='livro')),
    url(r'^calculo/',include(project+'.calculo.urls',namespace='calculo')),
    url(r'^servidor/',include(project+'.servidor.urls',namespace='servidor')),
    url(r'^documento/',include(project+'.documento.urls',namespace='documento')),
    url(r'^web/',include(project+'.web.urls',namespace='web')),
    url(r'^core/',include(project+'.core.urls',namespace='core')),


    # ACESSO AO PUBLICO
    url(r'^$', project+'.web.views_publicas.inicio'),
    url(r'^web/estatisticas/', project+'.web.estatisticas.estatisticas'),
    
    #INIT------------------------------SICOP---------------------------------------------------------------------------------
    
    # ACESSO RESTRITO SICOP PROCESSO
            
    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^sicop/processo/consulta/', 'TerraLegal.tramitacao.restrito.processo.consulta'),   
    url(r'^sicop/processo/cadastro/', 'TerraLegal.tramitacao.restrito.processo.cadastro'),
    url(r'^sicop/processo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.processo.edicao'),
    url(r'^sicop/processo/tramitacao/(?P<base>\d+)/', 'TerraLegal.tramitacao.restrito.processo.tramitar'),
    url(r'^sicop/processo/tramitacao_massa/', 'TerraLegal.tramitacao.restrito.processo.ativar_tramitacao_massa'),
    url(r'^sicop/processo/add_tramitacao_massa/(?P<base>\d+)/', 'TerraLegal.tramitacao.restrito.processo.add_tramitacao_massa'),
    url(r'^sicop/processo/rem_tramitacao_massa/(?P<base>\d+)/', 'TerraLegal.tramitacao.restrito.processo.rem_tramitacao_massa'),
    url(r'^sicop/processo/lista_tramitacao_massa/', 'TerraLegal.tramitacao.restrito.processo.executar_tramitacao_massa'),
    url(r'^sicop/processo/anexo/(?P<base>\d+)/', 'TerraLegal.tramitacao.restrito.processo.anexar'),
    url(r'^sicop/processo/pendencia/(?P<base>\d+)/', 'TerraLegal.tramitacao.restrito.processo.criar_pendencia'),   
    url(r'^sicop/processo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.processo.relatorio_pdf'),   
    url(r'^sicop/processo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.processo.relatorio_ods'),
    url(r'^sicop/processo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.processo.relatorio_csv'),
    url(r'^sicop/processo/desanexar/(?P<id_anexo>\d+)/', 'TerraLegal.tramitacao.restrito.processo.desanexar'),
    url(r'^sicop/processo/consultaProcesso/', 'TerraLegal.tramitacao.restrito.processo.consultaprocesso'),   
    

    # ACESSO RESTRITO SICOP PENDENCIA
    url(r'^sicop/pendencia/edicao/(?P<pendencia>\d+)/', 'TerraLegal.tramitacao.restrito.pendencia.edicao'),
    
    # PROCESSO RURAL
    url(r'^sicop/processo/rural/consulta/', 'TerraLegal.tramitacao.restrito.processo_rural.consulta'),
    url(r'^sicop/processo/rural/cadastro/', 'TerraLegal.tramitacao.restrito.processo_rural.cadastro'),
    url(r'^sicop/processo/rural/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.processo_rural.edicao'),
    # PROCESSO URBANO
    url(r'^sicop/processo/urbano/consulta/', 'TerraLegal.tramitacao.restrito.processo_urbano.consulta'),
    url(r'^sicop/processo/urbano/cadastro/', 'TerraLegal.tramitacao.restrito.processo_urbano.cadastro'),
    url(r'^sicop/processo/urbano/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.processo_urbano.edicao'),
    # PROCESSO CLAUSULA RESOLUTIVA
    url(r'^sicop/processo/clausula/consulta/', 'TerraLegal.tramitacao.restrito.processo_clausula.consulta'),
    url(r'^sicop/processo/clausula/cadastro/', 'TerraLegal.tramitacao.restrito.processo_clausula.cadastro'),
    url(r'^sicop/processo/clausula/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.processo_clausula.edicao'),
   
    
   # ACESSO RESTRITO SICOP PECA TECNICA 
    url(r'^sicop/peca_tecnica/consulta/', 'TerraLegal.tramitacao.restrito.peca_tecnica.consulta'),
    url(r'^sicop/peca_tecnica/cadastro/', 'TerraLegal.tramitacao.restrito.peca_tecnica.cadastro'),
    url(r'^sicop/peca_tecnica/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.peca_tecnica.edicao'),
    url(r'^sicop/peca_tecnica/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.peca_tecnica.relatorio_pdf'),
    url(r'^sicop/peca_tecnica/relatorio/ods/', 'TerraLegal.tramitacao.restrito.peca_tecnica.relatorio_ods'),
    url(r'^sicop/peca_tecnica/relatorio/csv/', 'TerraLegal.tramitacao.restrito.peca_tecnica.relatorio_csv'),

   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^sicop/contrato/consulta/', 'TerraLegal.tramitacao.restrito.contrato.consulta'),
    url(r'^sicop/contrato/cadastro/', 'TerraLegal.tramitacao.restrito.contrato.cadastro'),
    url(r'^sicop/contrato/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.contrato.edicao'),
    url(r'^sicop/contrato/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.contrato.relatorio_pdf'),    
    url(r'^sicop/contrato/relatorio/ods/', 'TerraLegal.tramitacao.restrito.contrato.relatorio_ods'),
    url(r'^sicop/contrato/relatorio/csv/', 'TerraLegal.tramitacao.restrito.contrato.relatorio_csv'),
 
   # ACESSO RESTRITO SICOP PREGAO 
    url(r'^sicop/pregao/consulta/', 'TerraLegal.tramitacao.restrito.pregao.consulta'),
    url(r'^sicop/pregao/cadastro/', 'TerraLegal.tramitacao.restrito.pregao.cadastro'),
    url(r'^sicop/pregao/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.pregao.edicao'),
    url(r'^sicop/pregao/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.pregao.relatorio_pdf'),    
    url(r'^sicop/pregao/relatorio/ods/', 'TerraLegal.tramitacao.restrito.pregao.relatorio_ods'),
    url(r'^sicop/pregao/relatorio/csv/', 'TerraLegal.tramitacao.restrito.pregao.relatorio_csv'),
    
    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/gleba/consulta/', 'TerraLegal.tramitacao.restrito.gleba.consulta'),
    url(r'^sicop/gleba/cadastro/', 'TerraLegal.tramitacao.restrito.gleba.cadastro'),
    url(r'^sicop/gleba/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.gleba.edicao'),
    url(r'^sicop/gleba/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.gleba.relatorio_pdf'),
    url(r'^sicop/gleba/relatorio/ods/', 'TerraLegal.tramitacao.restrito.gleba.relatorio_ods'),
    url(r'^sicop/gleba/relatorio/csv/', 'TerraLegal.tramitacao.restrito.gleba.relatorio_csv'),

    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/caixa/consulta/', 'TerraLegal.tramitacao.restrito.caixa.consulta'),
    url(r'^sicop/caixa/cadastro/', 'TerraLegal.tramitacao.restrito.caixa.cadastro'),
    url(r'^sicop/caixa/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.caixa.edicao'),
    url(r'^sicop/caixa/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.caixa.relatorio_pdf'),
    url(r'^sicop/caixa/relatorio/ods/', 'TerraLegal.tramitacao.restrito.caixa.relatorio_ods'),
    url(r'^sicop/caixa/relatorio/csv/', 'TerraLegal.tramitacao.restrito.caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP ETAPA
    url(r'^sicop/etapa/consulta/', 'TerraLegal.tramitacao.restrito.etapa.consulta'),
    url(r'^sicop/etapa/cadastro/', 'TerraLegal.tramitacao.restrito.etapa.cadastro'),
    url(r'^sicop/etapa/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.etapa.edicao'),
    url(r'^sicop/etapa/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.etapa.relatorio_pdf'),
    url(r'^sicop/etapa/relatorio/ods/', 'TerraLegal.tramitacao.restrito.etapa.relatorio_ods'),
    url(r'^sicop/etapa/relatorio/csv/', 'TerraLegal.tramitacao.restrito.etapa.relatorio_csv'),
    url(r'^sicop/etapa/checklist/(?P<processo>\d+)/(?P<etapa>\d+)/', 'TerraLegal.tramitacao.restrito.etapa.checklist'),
    url(r'^sicop/etapa/restaurar/(?P<processo>\d+)/', 'TerraLegal.tramitacao.restrito.etapa.restaurar'),

    # ACESSO RESTRITO SICOP CHECKLIST
    url(r'^sicop/checklist/consulta/', 'TerraLegal.tramitacao.restrito.checklist.consulta'),
    url(r'^sicop/checklist/cadastro/', 'TerraLegal.tramitacao.restrito.checklist.cadastro'),
    url(r'^sicop/checklist/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.checklist.edicao'),
    url(r'^sicop/checklist/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.checklist.relatorio_pdf'),
    url(r'^sicop/checklist/relatorio/ods/', 'TerraLegal.tramitacao.restrito.checklist.relatorio_ods'),
    url(r'^sicop/checklist/relatorio/csv/', 'TerraLegal.tramitacao.restrito.checklist.relatorio_csv'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/sub_area/consulta/', 'TerraLegal.tramitacao.restrito.sub_area.consulta'),
    url(r'^sicop/sub_area/cadastro/', 'TerraLegal.tramitacao.restrito.sub_area.cadastro'),
    url(r'^sicop/sub_area/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.sub_area.edicao'),
    url(r'^sicop/sub_area/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.sub_area.relatorio_pdf'),
    url(r'^sicop/sub_area/relatorio/ods/', 'TerraLegal.tramitacao.restrito.sub_area.relatorio_ods'),
    url(r'^sicop/sub_area/relatorio/csv/', 'TerraLegal.tramitacao.restrito.sub_area.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/tipo_caixa/consulta/', 'TerraLegal.tramitacao.restrito.tipo_caixa.consulta'),
    url(r'^sicop/tipo_caixa/cadastro/', 'TerraLegal.tramitacao.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/tipo_caixa/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.tipo_caixa.edicao'),
    url(r'^sicop/tipo_caixa/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.tipo_caixa.relatorio_pdf'),
    url(r'^sicop/tipo_caixa/relatorio/ods/', 'TerraLegal.tramitacao.restrito.tipo_caixa.relatorio_ods'),
    url(r'^sicop/tipo_caixa/relatorio/csv/', 'TerraLegal.tramitacao.restrito.tipo_caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/tipo_processo/consulta/', 'TerraLegal.tramitacao.restrito.tipo_processo.consulta'),
    url(r'^sicop/tipo_processo/cadastro/', 'TerraLegal.tramitacao.restrito.tipo_processo.cadastro'),
    url(r'^sicop/tipo_processo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.tipo_processo.edicao'),
    url(r'^sicop/tipo_processo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.tipo_processo.relatorio_pdf'),
    url(r'^sicop/tipo_processo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.tipo_processo.relatorio_ods'),
    url(r'^sicop/tipo_processo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.tipo_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/tipo_pendencia/consulta/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/tipo_pendencia/cadastro/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/tipo_pendencia/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.edicao'),
    url(r'^sicop/tipo_pendencia/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.relatorio_pdf'),
    url(r'^sicop/tipo_pendencia/relatorio/ods/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.relatorio_ods'),
    url(r'^sicop/tipo_pendencia/relatorio/csv/', 'TerraLegal.tramitacao.restrito.tipo_pendencia.relatorio_csv'),

    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^sicop/situacao_processo/consulta/', 'TerraLegal.tramitacao.restrito.situacao_processo.consulta'),
    url(r'^sicop/situacao_processo/cadastro/', 'TerraLegal.tramitacao.restrito.situacao_processo.cadastro'),
    url(r'^sicop/situacao_processo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.situacao_processo.edicao'),
    url(r'^sicop/situacao_processo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.situacao_processo.relatorio_pdf'),
    url(r'^sicop/situacao_processo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.situacao_processo.relatorio_ods'),
    url(r'^sicop/situacao_processo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.situacao_processo.relatorio_csv'),


    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^sicop/situacao_geo/consulta/', 'TerraLegal.tramitacao.restrito.situacao_geo.consulta'),
    url(r'^sicop/situacao_geo/cadastro/', 'TerraLegal.tramitacao.restrito.situacao_geo.cadastro'),
    url(r'^sicop/situacao_geo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.situacao_geo.edicao'),
    url(r'^sicop/situacao_geo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.situacao_geo.relatorio_pdf'),
    url(r'^sicop/situacao_geo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.situacao_geo.relatorio_ods'),
    url(r'^sicop/situacao_geo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.situacao_geo.relatorio_csv'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^sicop/classificacao_processo/consulta/', 'TerraLegal.tramitacao.restrito.classificacao_processo.consulta'),
    url(r'^sicop/classificacao_processo/cadastro/', 'TerraLegal.tramitacao.restrito.classificacao_processo.cadastro'),
    url(r'^sicop/classificacao_processo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.classificacao_processo.edicao'),
    url(r'^sicop/classificacao_processo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.classificacao_processo.relatorio_pdf'),
    url(r'^sicop/classificacao_processo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.classificacao_processo.relatorio_ods'),
    url(r'^sicop/classificacao_processo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.classificacao_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^sicop/status_pendencia/consulta/', 'TerraLegal.tramitacao.restrito.status_pendencia.consulta'),
    url(r'^sicop/status_pendencia/cadastro/', 'TerraLegal.tramitacao.restrito.status_pendencia.cadastro'),
    url(r'^sicop/status_pendencia/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.status_pendencia.edicao'),
    url(r'^sicop/status_pendencia/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.status_pendencia.relatorio_pdf'),
    url(r'^sicop/status_pendencia/relatorio/ods/', 'TerraLegal.tramitacao.restrito.status_pendencia.relatorio_ods'),
    url(r'^sicop/status_pendencia/relatorio/csv/', 'TerraLegal.tramitacao.restrito.status_pendencia.relatorio_csv'),

   # ACESSO RESTRITO SICOP DIVISAO
    url(r'^sicop/divisao/consulta/', 'TerraLegal.tramitacao.restrito.divisao.consulta'),
    url(r'^sicop/divisao/cadastro/', 'TerraLegal.tramitacao.restrito.divisao.cadastro'),
    url(r'^sicop/divisao/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.divisao.edicao'),
    url(r'^sicop/divisao/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.divisao.relatorio_pdf'),
    url(r'^sicop/divisao/relatorio/ods/', 'TerraLegal.tramitacao.restrito.divisao.relatorio_ods'),
    url(r'^sicop/divisao/relatorio/csv/', 'TerraLegal.tramitacao.restrito.divisao.relatorio_csv'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^sicop/grupo/consulta/', 'TerraLegal.tramitacao.restrito.grupo.consulta'),
    url(r'^sicop/grupo/cadastro/', 'TerraLegal.tramitacao.restrito.grupo.cadastro'),
    url(r'^sicop/grupo/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.grupo.edicao'),
    url(r'^sicop/grupo/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.grupo.relatorio_pdf'),
    url(r'^sicop/grupo/relatorio/ods/', 'TerraLegal.tramitacao.restrito.grupo.relatorio_ods'),
    url(r'^sicop/grupo/relatorio/csv/', 'TerraLegal.tramitacao.restrito.grupo.relatorio_csv'),

  # ACESSO RESTRITO SICOP PERMISSAO
    url(r'^sicop/permissao/consulta/', 'TerraLegal.tramitacao.restrito.permissao.consulta'),
    url(r'^sicop/permissao/cadastro/', 'TerraLegal.tramitacao.restrito.permissao.cadastro'),
    url(r'^sicop/permissao/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.permissao.edicao'),
    url(r'^sicop/permissao/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.permissao.relatorio_pdf'),
    url(r'^sicop/permissao/relatorio/ods/', 'TerraLegal.tramitacao.restrito.permissao.relatorio_ods'),
    url(r'^sicop/permissao/relatorio/csv/', 'TerraLegal.tramitacao.restrito.permissao.relatorio_csv'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^sicop/usuario/consulta/', 'TerraLegal.tramitacao.restrito.usuario.consulta'),
    url(r'^sicop/usuario/cadastro/', 'TerraLegal.tramitacao.restrito.usuario.cadastro'),
    url(r'^sicop/usuario/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.usuario.edicao'),
    url(r'^sicop/usuario/edicao/usuario/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.usuario.edicao_usuario_logado'),
    url(r'^sicop/usuario/relatorio/pdf/', 'TerraLegal.tramitacao.restrito.usuario.relatorio_pdf'),
    url(r'^sicop/usuario/relatorio/ods/', 'TerraLegal.tramitacao.restrito.usuario.relatorio_ods'),
    url(r'^sicop/usuario/relatorio/csv/', 'TerraLegal.tramitacao.restrito.usuario.relatorio_csv'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    
    url(r'^sicop/municipio/consulta/', 'TerraLegal.tramitacao.restrito.municipio.consulta'),
    url(r'^sicop/municipio/edicao/(?P<id>\d+)/', 'TerraLegal.tramitacao.restrito.municipio.edicao'),
   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^sicop/relatorio/lista', 'TerraLegal.tramitacao.restrito.relatorio.lista'),
    url(r'^sicop/relatorio/processos', 'TerraLegal.tramitacao.restrito.relatorio.processos'),
    url(r'^sicop/relatorio/processo_peca', 'TerraLegal.tramitacao.restrito.relatorio.processo_peca'),
    url(r'^sicop/relatorio/processo_sem_peca', 'TerraLegal.tramitacao.restrito.relatorio.processo_sem_peca'),
    url(r'^sicop/relatorio/peca_processo', 'TerraLegal.tramitacao.restrito.relatorio.peca_processo'),
    url(r'^sicop/relatorio/peca_gleba', 'TerraLegal.tramitacao.restrito.relatorio.peca_gleba'),
    url(r'^sicop/relatorio/peca_nao_aprovada', 'TerraLegal.tramitacao.restrito.relatorio.peca_nao_aprovada'),
    url(r'^sicop/relatorio/peca_rejeitada', 'TerraLegal.tramitacao.restrito.relatorio.peca_rejeitada'),
    url(r'^sicop/relatorio/peca_sem_processo', 'TerraLegal.tramitacao.restrito.relatorio.peca_sem_processo'),
    url(r'^sicop/relatorio/peca_validada', 'TerraLegal.tramitacao.restrito.relatorio.peca_validada'),
    url(r'^sicop/relatorio/peca', 'TerraLegal.tramitacao.restrito.relatorio.pecas'),
    
    url(r'^sicop/relatorio/etapa/p23', 'TerraLegal.tramitacao.restrito.relatorio.etapa_p23'),
    url(r'^sicop/relatorio/etapa/p80', 'TerraLegal.tramitacao.restrito.relatorio.etapa_p80'),
    url(r'^sicop/relatorio/etapa/urbano', 'TerraLegal.tramitacao.restrito.relatorio.etapa_urbano'),
    
    #END------------------------------SICOP---------------------------------------------------------------------------------
   
    # ACESSO RESTRITO TABELA SITUACAO 
    url(r'^sicop/situacao/consulta/', 'TerraLegal.tramitacao.restrito.situacao.consulta'),
    url(r'^sicop/situacao/edicao/(?P<id>\d+)/','TerraLegal.tramitacao.restrito.situacao.edicao'),
    url(r'^sicop/situacao/cadastro/', 'TerraLegal.tramitacao.restrito.situacao.cadastro'),
    #END------------------------------CONTROLE---------------------------------------------------------------------------------
        
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
