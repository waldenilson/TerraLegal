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
    url(r'^servidor/',include('servidor.urls',namespace='servidor')),
    url(r'^web/',include(project+'.web.urls',namespace='web')),
    url(r'^core/',include(project+'.core.urls',namespace='core')),


    # ACESSO AO PUBLICO
    url(r'^$', project+'.web.views_publicas.inicio'),
    url(r'^web/estatisticas/', project+'.web.estatisticas.estatisticas'),
    
    #INIT------------------------------SICOP---------------------------------------------------------------------------------
    
    # ACESSO RESTRITO SICOP PROCESSO

    # ESCOLHA DO TIPO DE DOCUMENTO
    url(r'^sicop/restrito/documento/consulta/', 'sicop.restrito.documento.consulta'),   
    url(r'^sicop/restrito/documento/cadastro/', 'sicop.restrito.documento.cadastro'),
    url(r'^sicop/restrito/documento/edicao/(?P<id>\d+)/', 'sicop.restrito.documento.edicao'),

    # ESCOLHA DO TIPO DE DOCUMENTO
    url(r'^sicop/restrito/tipo_documento/consulta/', 'sicop.restrito.tipo_documento.consulta'),   
    url(r'^sicop/restrito/tipo_documento/cadastro/', 'sicop.restrito.tipo_documento.cadastro'),
    url(r'^sicop/restrito/tipo_documento/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_documento.edicao'),
    
    # DOCUMENTO MEMORANDO
    url(r'^sicop/restrito/documento/memorando/consulta/', 'sicop.restrito.documento_memorando.consulta'),
    url(r'^sicop/restrito/documento/memorando/cadastro/', 'sicop.restrito.documento_memorando.cadastro'),
    url(r'^sicop/restrito/documento/memorando/edicao/(?P<id>\d+)/', 'sicop.restrito.documento_memorando.edicao'),
    url(r'^sicop/restrito/documento/memorando/criacao/(?P<id>\d+)/', 'sicop.restrito.documento_memorando.criacao'),

    # DOCUMENTO OFICIO
    url(r'^sicop/restrito/documento/oficio/consulta/', 'sicop.restrito.documento_oficio.consulta'),
    url(r'^sicop/restrito/documento/oficio/cadastro/', 'sicop.restrito.documento_oficio.cadastro'),
    url(r'^sicop/restrito/documento/oficio/edicao/(?P<id>\d+)/', 'sicop.restrito.documento_oficio.edicao'),
    url(r'^sicop/restrito/documento/oficio/criacao/(?P<id>\d+)/', 'sicop.restrito.documento_oficio.criacao'),
    
    # DOCUMENTO REQUISICAO DE VIATURA
    url(r'^sicop/restrito/documento/requisicao_viatura/consulta/', 'sicop.restrito.documento_requisicao_viatura.consulta'),
    url(r'^sicop/restrito/documento/requisicao_viatura/cadastro/', 'sicop.restrito.documento_requisicao_viatura.cadastro'),
    url(r'^sicop/restrito/documento/requisicao_viatura/edicao/(?P<id>\d+)/', 'sicop.restrito.documento_requisicao_viatura.edicao'),
    url(r'^sicop/restrito/documento/requisicao_viatura/criacao/(?P<id>\d+)/', 'sicop.restrito.documento_requisicao_viatura.criacao'),
    
    # DOCUMENTO RME
    url(r'^sicop/restrito/documento/rme/consulta/', 'sicop.restrito.documento_rme.consulta'),
    url(r'^sicop/restrito/documento/rme/cadastro/', 'sicop.restrito.documento_rme.cadastro'),
    url(r'^sicop/restrito/documento/rme/edicao/(?P<id>\d+)/', 'sicop.restrito.documento_rme.edicao'),
    url(r'^sicop/restrito/documento/rme/criacao/(?P<id>\d+)/', 'sicop.restrito.documento_rme.criacao'),
    url(r'^sicop/restrito/documento/rme/material/(?P<doc>\d+)/', 'sicop.restrito.documento_rme.criar_material'),
    url(r'^sicop/restrito/documento/rme/material/edicao/(?P<materialrme>\d+)/', 'sicop.restrito.materialrme.edicao'),
       
        
    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^sicop/restrito/processo/consulta/', 'sicop.restrito.processo.consulta'),   
    url(r'^sicop/restrito/processo/cadastro/', 'sicop.restrito.processo.cadastro'),
    url(r'^sicop/restrito/processo/edicao/(?P<id>\d+)/', 'sicop.restrito.processo.edicao'),
    url(r'^sicop/restrito/processo/tramitacao/(?P<base>\d+)/', 'sicop.restrito.processo.tramitar'),
    url(r'^sicop/restrito/processo/tramitacao_massa/', 'sicop.restrito.processo.ativar_tramitacao_massa'),
    url(r'^sicop/restrito/processo/add_tramitacao_massa/(?P<base>\d+)/', 'sicop.restrito.processo.add_tramitacao_massa'),
    url(r'^sicop/restrito/processo/rem_tramitacao_massa/(?P<base>\d+)/', 'sicop.restrito.processo.rem_tramitacao_massa'),
    url(r'^sicop/restrito/processo/lista_tramitacao_massa/', 'sicop.restrito.processo.executar_tramitacao_massa'),
    url(r'^sicop/restrito/processo/anexo/(?P<base>\d+)/', 'sicop.restrito.processo.anexar'),
    url(r'^sicop/restrito/processo/pendencia/(?P<base>\d+)/', 'sicop.restrito.processo.criar_pendencia'),   
    url(r'^sicop/restrito/processo/relatorio/pdf/', 'sicop.restrito.processo.relatorio_pdf'),   
    url(r'^sicop/restrito/processo/relatorio/ods/', 'sicop.restrito.processo.relatorio_ods'),
    url(r'^sicop/restrito/processo/relatorio/csv/', 'sicop.restrito.processo.relatorio_csv'),
    url(r'^sicop/restrito/processo/desanexar/(?P<id_anexo>\d+)/', 'sicop.restrito.processo.desanexar'),

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
    url(r'^sicop/restrito/peca_tecnica/relatorio/pdf/', 'sicop.restrito.peca_tecnica.relatorio_pdf'),
    url(r'^sicop/restrito/peca_tecnica/relatorio/ods/', 'sicop.restrito.peca_tecnica.relatorio_ods'),
    url(r'^sicop/restrito/peca_tecnica/relatorio/csv/', 'sicop.restrito.peca_tecnica.relatorio_csv'),

   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^sicop/restrito/contrato/consulta/', 'sicop.restrito.contrato.consulta'),
    url(r'^sicop/restrito/contrato/cadastro/', 'sicop.restrito.contrato.cadastro'),
    url(r'^sicop/restrito/contrato/edicao/(?P<id>\d+)/', 'sicop.restrito.contrato.edicao'),
    url(r'^sicop/restrito/contrato/relatorio/pdf/', 'sicop.restrito.contrato.relatorio_pdf'),    
    url(r'^sicop/restrito/contrato/relatorio/ods/', 'sicop.restrito.contrato.relatorio_ods'),
    url(r'^sicop/restrito/contrato/relatorio/csv/', 'sicop.restrito.contrato.relatorio_csv'),
 
   # ACESSO RESTRITO SICOP PREGAO 
    url(r'^sicop/restrito/pregao/consulta/', 'sicop.restrito.pregao.consulta'),
    url(r'^sicop/restrito/pregao/cadastro/', 'sicop.restrito.pregao.cadastro'),
    url(r'^sicop/restrito/pregao/edicao/(?P<id>\d+)/', 'sicop.restrito.pregao.edicao'),
    url(r'^sicop/restrito/pregao/relatorio/pdf/', 'sicop.restrito.pregao.relatorio_pdf'),    
    url(r'^sicop/restrito/pregao/relatorio/ods/', 'sicop.restrito.pregao.relatorio_ods'),
    url(r'^sicop/restrito/pregao/relatorio/csv/', 'sicop.restrito.pregao.relatorio_csv'),
    
    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/restrito/gleba/consulta/', 'sicop.restrito.gleba.consulta'),
    url(r'^sicop/restrito/gleba/cadastro/', 'sicop.restrito.gleba.cadastro'),
    url(r'^sicop/restrito/gleba/edicao/(?P<id>\d+)/', 'sicop.restrito.gleba.edicao'),
    url(r'^sicop/restrito/gleba/relatorio/pdf/', 'sicop.restrito.gleba.relatorio_pdf'),
    url(r'^sicop/restrito/gleba/relatorio/ods/', 'sicop.restrito.gleba.relatorio_ods'),
    url(r'^sicop/restrito/gleba/relatorio/csv/', 'sicop.restrito.gleba.relatorio_csv'),

    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/restrito/caixa/consulta/', 'sicop.restrito.caixa.consulta'),
    url(r'^sicop/restrito/caixa/cadastro/', 'sicop.restrito.caixa.cadastro'),
    url(r'^sicop/restrito/caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.caixa.edicao'),
    url(r'^sicop/restrito/caixa/relatorio/pdf/', 'sicop.restrito.caixa.relatorio_pdf'),
    url(r'^sicop/restrito/caixa/relatorio/ods/', 'sicop.restrito.caixa.relatorio_ods'),
    url(r'^sicop/restrito/caixa/relatorio/csv/', 'sicop.restrito.caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP ETAPA
    url(r'^sicop/restrito/etapa/consulta/', 'sicop.restrito.etapa.consulta'),
    url(r'^sicop/restrito/etapa/cadastro/', 'sicop.restrito.etapa.cadastro'),
    url(r'^sicop/restrito/etapa/edicao/(?P<id>\d+)/', 'sicop.restrito.etapa.edicao'),
    url(r'^sicop/restrito/etapa/relatorio/pdf/', 'sicop.restrito.etapa.relatorio_pdf'),
    url(r'^sicop/restrito/etapa/relatorio/ods/', 'sicop.restrito.etapa.relatorio_ods'),
    url(r'^sicop/restrito/etapa/relatorio/csv/', 'sicop.restrito.etapa.relatorio_csv'),
    url(r'^sicop/restrito/etapa/checklist/(?P<processo>\d+)/(?P<etapa>\d+)/', 'sicop.restrito.etapa.checklist'),
    url(r'^sicop/restrito/etapa/restaurar/(?P<processo>\d+)/', 'sicop.restrito.etapa.restaurar'),

    # ACESSO RESTRITO SICOP CHECKLIST
    url(r'^sicop/restrito/checklist/consulta/', 'sicop.restrito.checklist.consulta'),
    url(r'^sicop/restrito/checklist/cadastro/', 'sicop.restrito.checklist.cadastro'),
    url(r'^sicop/restrito/checklist/edicao/(?P<id>\d+)/', 'sicop.restrito.checklist.edicao'),
    url(r'^sicop/restrito/checklist/relatorio/pdf/', 'sicop.restrito.checklist.relatorio_pdf'),
    url(r'^sicop/restrito/checklist/relatorio/ods/', 'sicop.restrito.checklist.relatorio_ods'),
    url(r'^sicop/restrito/checklist/relatorio/csv/', 'sicop.restrito.checklist.relatorio_csv'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/restrito/sub_area/consulta/', 'sicop.restrito.sub_area.consulta'),
    url(r'^sicop/restrito/sub_area/cadastro/', 'sicop.restrito.sub_area.cadastro'),
    url(r'^sicop/restrito/sub_area/edicao/(?P<id>\d+)/', 'sicop.restrito.sub_area.edicao'),
    url(r'^sicop/restrito/sub_area/relatorio/pdf/', 'sicop.restrito.sub_area.relatorio_pdf'),
    url(r'^sicop/restrito/sub_area/relatorio/ods/', 'sicop.restrito.sub_area.relatorio_ods'),
    url(r'^sicop/restrito/sub_area/relatorio/csv/', 'sicop.restrito.sub_area.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/restrito/tipo_caixa/consulta/', 'sicop.restrito.tipo_caixa.consulta'),
    url(r'^sicop/restrito/tipo_caixa/cadastro/', 'sicop.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/restrito/tipo_caixa/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_caixa.edicao'),
    url(r'^sicop/restrito/tipo_caixa/relatorio/pdf/', 'sicop.restrito.tipo_caixa.relatorio_pdf'),
    url(r'^sicop/restrito/tipo_caixa/relatorio/ods/', 'sicop.restrito.tipo_caixa.relatorio_ods'),
    url(r'^sicop/restrito/tipo_caixa/relatorio/csv/', 'sicop.restrito.tipo_caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/restrito/tipo_processo/consulta/', 'sicop.restrito.tipo_processo.consulta'),
    url(r'^sicop/restrito/tipo_processo/cadastro/', 'sicop.restrito.tipo_processo.cadastro'),
    url(r'^sicop/restrito/tipo_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_processo.edicao'),
    url(r'^sicop/restrito/tipo_processo/relatorio/pdf/', 'sicop.restrito.tipo_processo.relatorio_pdf'),
    url(r'^sicop/restrito/tipo_processo/relatorio/ods/', 'sicop.restrito.tipo_processo.relatorio_ods'),
    url(r'^sicop/restrito/tipo_processo/relatorio/csv/', 'sicop.restrito.tipo_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO DOCUMENTO
    url(r'^sicop/restrito/tipo_documento/consulta/', 'sicop.restrito.tipo_documento.consulta'),
    url(r'^sicop/restrito/tipo_documento/cadastro/', 'sicop.restrito.tipo_documento.cadastro'),
    url(r'^sicop/restrito/tipo_documento/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_documento.edicao'),
    url(r'^sicop/restrito/tipo_documento/relatorio/pdf/', 'sicop.restrito.tipo_documento.relatorio_pdf'),
    url(r'^sicop/restrito/tipo_documento/relatorio/ods/', 'sicop.restrito.tipo_documento.relatorio_ods'),
    url(r'^sicop/restrito/tipo_documento/relatorio/csv/', 'sicop.restrito.tipo_documento.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/restrito/tipo_pendencia/consulta/', 'sicop.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/restrito/tipo_pendencia/cadastro/', 'sicop.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/restrito/tipo_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.tipo_pendencia.edicao'),
    url(r'^sicop/restrito/tipo_pendencia/relatorio/pdf/', 'sicop.restrito.tipo_pendencia.relatorio_pdf'),
    url(r'^sicop/restrito/tipo_pendencia/relatorio/ods/', 'sicop.restrito.tipo_pendencia.relatorio_ods'),
    url(r'^sicop/restrito/tipo_pendencia/relatorio/csv/', 'sicop.restrito.tipo_pendencia.relatorio_csv'),

    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^sicop/restrito/situacao_processo/consulta/', 'sicop.restrito.situacao_processo.consulta'),
    url(r'^sicop/restrito/situacao_processo/cadastro/', 'sicop.restrito.situacao_processo.cadastro'),
    url(r'^sicop/restrito/situacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_processo.edicao'),
    url(r'^sicop/restrito/situacao_processo/relatorio/pdf/', 'sicop.restrito.situacao_processo.relatorio_pdf'),
    url(r'^sicop/restrito/situacao_processo/relatorio/ods/', 'sicop.restrito.situacao_processo.relatorio_ods'),
    url(r'^sicop/restrito/situacao_processo/relatorio/csv/', 'sicop.restrito.situacao_processo.relatorio_csv'),


    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^sicop/restrito/situacao_geo/consulta/', 'sicop.restrito.situacao_geo.consulta'),
    url(r'^sicop/restrito/situacao_geo/cadastro/', 'sicop.restrito.situacao_geo.cadastro'),
    url(r'^sicop/restrito/situacao_geo/edicao/(?P<id>\d+)/', 'sicop.restrito.situacao_geo.edicao'),
    url(r'^sicop/restrito/situacao_geo/relatorio/pdf/', 'sicop.restrito.situacao_geo.relatorio_pdf'),
    url(r'^sicop/restrito/situacao_geo/relatorio/ods/', 'sicop.restrito.situacao_geo.relatorio_ods'),
    url(r'^sicop/restrito/situacao_geo/relatorio/csv/', 'sicop.restrito.situacao_geo.relatorio_csv'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^sicop/restrito/classificacao_processo/consulta/', 'sicop.restrito.classificacao_processo.consulta'),
    url(r'^sicop/restrito/classificacao_processo/cadastro/', 'sicop.restrito.classificacao_processo.cadastro'),
    url(r'^sicop/restrito/classificacao_processo/edicao/(?P<id>\d+)/', 'sicop.restrito.classificacao_processo.edicao'),
    url(r'^sicop/restrito/classificacao_processo/relatorio/pdf/', 'sicop.restrito.classificacao_processo.relatorio_pdf'),
    url(r'^sicop/restrito/classificacao_processo/relatorio/ods/', 'sicop.restrito.classificacao_processo.relatorio_ods'),
    url(r'^sicop/restrito/classificacao_processo/relatorio/csv/', 'sicop.restrito.classificacao_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^sicop/restrito/status_pendencia/consulta/', 'sicop.restrito.status_pendencia.consulta'),
    url(r'^sicop/restrito/status_pendencia/cadastro/', 'sicop.restrito.status_pendencia.cadastro'),
    url(r'^sicop/restrito/status_pendencia/edicao/(?P<id>\d+)/', 'sicop.restrito.status_pendencia.edicao'),
    url(r'^sicop/restrito/status_pendencia/relatorio/pdf/', 'sicop.restrito.status_pendencia.relatorio_pdf'),
    url(r'^sicop/restrito/status_pendencia/relatorio/ods/', 'sicop.restrito.status_pendencia.relatorio_ods'),
    url(r'^sicop/restrito/status_pendencia/relatorio/csv/', 'sicop.restrito.status_pendencia.relatorio_csv'),

   # ACESSO RESTRITO SICOP DIVISAO
    url(r'^sicop/restrito/divisao/consulta/', 'sicop.restrito.divisao.consulta'),
    url(r'^sicop/restrito/divisao/cadastro/', 'sicop.restrito.divisao.cadastro'),
    url(r'^sicop/restrito/divisao/edicao/(?P<id>\d+)/', 'sicop.restrito.divisao.edicao'),
    url(r'^sicop/restrito/divisao/relatorio/pdf/', 'sicop.restrito.divisao.relatorio_pdf'),
    url(r'^sicop/restrito/divisao/relatorio/ods/', 'sicop.restrito.divisao.relatorio_ods'),
    url(r'^sicop/restrito/divisao/relatorio/csv/', 'sicop.restrito.divisao.relatorio_csv'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^sicop/restrito/grupo/consulta/', 'sicop.restrito.grupo.consulta'),
    url(r'^sicop/restrito/grupo/cadastro/', 'sicop.restrito.grupo.cadastro'),
    url(r'^sicop/restrito/grupo/edicao/(?P<id>\d+)/', 'sicop.restrito.grupo.edicao'),
    url(r'^sicop/restrito/grupo/relatorio/pdf/', 'sicop.restrito.grupo.relatorio_pdf'),
    url(r'^sicop/restrito/grupo/relatorio/ods/', 'sicop.restrito.grupo.relatorio_ods'),
    url(r'^sicop/restrito/grupo/relatorio/csv/', 'sicop.restrito.grupo.relatorio_csv'),

  # ACESSO RESTRITO SICOP PERMISSAO
    url(r'^sicop/restrito/permissao/consulta/', 'sicop.restrito.permissao.consulta'),
    url(r'^sicop/restrito/permissao/cadastro/', 'sicop.restrito.permissao.cadastro'),
    url(r'^sicop/restrito/permissao/edicao/(?P<id>\d+)/', 'sicop.restrito.permissao.edicao'),
    url(r'^sicop/restrito/permissao/relatorio/pdf/', 'sicop.restrito.permissao.relatorio_pdf'),
    url(r'^sicop/restrito/permissao/relatorio/ods/', 'sicop.restrito.permissao.relatorio_ods'),
    url(r'^sicop/restrito/permissao/relatorio/csv/', 'sicop.restrito.permissao.relatorio_csv'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^sicop/restrito/usuario/consulta/', 'sicop.restrito.usuario.consulta'),
    url(r'^sicop/restrito/usuario/cadastro/', 'sicop.restrito.usuario.cadastro'),
    url(r'^sicop/restrito/usuario/edicao/(?P<id>\d+)/', 'sicop.restrito.usuario.edicao'),
    url(r'^sicop/restrito/usuario/edicao/usuario/(?P<id>\d+)/', 'sicop.restrito.usuario.edicao_usuario_logado'),
    url(r'^sicop/restrito/usuario/relatorio/pdf/', 'sicop.restrito.usuario.relatorio_pdf'),
    url(r'^sicop/restrito/usuario/relatorio/ods/', 'sicop.restrito.usuario.relatorio_ods'),
    url(r'^sicop/restrito/usuario/relatorio/csv/', 'sicop.restrito.usuario.relatorio_csv'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    
    url(r'^sicop/restrito/municipio/consulta/', 'sicop.restrito.municipio.consulta'),
    url(r'^sicop/restrito/municipio/edicao/(?P<id>\d+)/', 'sicop.restrito.municipio.edicao'),
   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^sicop/restrito/relatorio/lista', 'sicop.restrito.relatorio.lista'),
    url(r'^sicop/restrito/relatorio/processo_peca', 'sicop.restrito.relatorio.processo_peca'),
    url(r'^sicop/restrito/relatorio/peca_processo', 'sicop.restrito.relatorio.peca_processo'),
    url(r'^sicop/restrito/relatorio/peca_gleba', 'sicop.restrito.relatorio.peca_gleba'),
    url(r'^sicop/restrito/relatorio/peca_nao_aprovada', 'sicop.restrito.relatorio.peca_nao_aprovada'),
    url(r'^sicop/restrito/relatorio/peca_rejeitada', 'sicop.restrito.relatorio.peca_rejeitada'),
    url(r'^sicop/restrito/relatorio/peca_sem_processo', 'sicop.restrito.relatorio.peca_sem_processo'),
    url(r'^sicop/restrito/relatorio/peca_validada', 'sicop.restrito.relatorio.peca_validada'),
    url(r'^sicop/restrito/relatorio/peca', 'sicop.restrito.relatorio.pecas'),
    #END------------------------------SICOP---------------------------------------------------------------------------------
   
    # ACESSO RESTRITO TABELA SITUACAO 
    url(r'^sicop/restrito/situacao/consulta/', 'sicop.restrito.situacao.consulta'),
    url(r'^sicop/restrito/situacao/edicao/(?P<id>\d+)/','sicop.restrito.situacao.edicao'),
    url(r'^sicop/restrito/situacao/cadastro/', 'sicop.restrito.situacao.cadastro'),
    #END------------------------------CONTROLE---------------------------------------------------------------------------------
        
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
