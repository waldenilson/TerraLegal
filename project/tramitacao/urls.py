# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('project.tramitacao',

   # ACESSO RESTRITO SICOP CONTRATO 
    url(r'^contrato/consulta/', 'restrito.contrato.consulta'),
    url(r'^contrato/cadastro/', 'restrito.contrato.cadastro'),
    url(r'^contrato/edicao/(?P<id>\d+)/', 'restrito.contrato.edicao'),

   # ACESSO RESTRITO SICOP PREGAO 
    url(r'^pregao/consulta/', 'restrito.pregao.consulta'),
    url(r'^pregao/cadastro/', 'restrito.pregao.cadastro'),
    url(r'^pregao/edicao/(?P<id>\d+)/', 'restrito.pregao.edicao'),

    # ACESSO RESTRITO SICOP GLEBA
    url(r'^gleba/consulta/', 'restrito.gleba.consulta'),
    url(r'^gleba/cadastro/', 'restrito.gleba.cadastro'),
    url(r'^gleba/edicao/(?P<id>\d+)/', 'restrito.gleba.edicao'),
    
    # ACESSO RESTRITO SICOP CAIXA
    url(r'^caixa/consulta/', 'restrito.caixa.consulta'),
    url(r'^caixa/cadastro/', 'restrito.caixa.cadastro'),
    url(r'^caixa/edicao/(?P<id>\d+)/', 'restrito.caixa.edicao'),
    url(r'^caixa/relatorio/pdf/', 'restrito.caixa.relatorio_pdf'),
    url(r'^caixa/relatorio/ods/', 'restrito.caixa.relatorio_ods'),
    url(r'^caixa/relatorio/titulo/ods/', 'restrito.caixa.relatorio_titulo_ods'),
    url(r'^caixa/relatorio/csv/', 'restrito.caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP ETAPA
    url(r'^etapa/consulta/', 'restrito.etapa.consulta'),
    url(r'^etapa/cadastro/', 'restrito.etapa.cadastro'),
    url(r'^etapa/edicao/(?P<id>\d+)/', 'restrito.etapa.edicao'),
    url(r'^etapa/relatorio/pdf/', 'restrito.etapa.relatorio_pdf'),
    url(r'^etapa/relatorio/ods/', 'restrito.etapa.relatorio_ods'),
    url(r'^etapa/relatorio/csv/', 'restrito.etapa.relatorio_csv'),
    url(r'^etapa/checklist/(?P<processo>\d+)/(?P<etapa>\d+)/', 'restrito.etapa.checklist'),
    url(r'^etapa/restaurar/(?P<processo>\d+)/', 'restrito.etapa.restaurar'),

    # ACESSO RESTRITO SICOP CHECKLIST
    url(r'^checklist/consulta/', 'restrito.checklist.consulta'),
    url(r'^checklist/cadastro/', 'restrito.checklist.cadastro'),
    url(r'^checklist/edicao/(?P<id>\d+)/', 'restrito.checklist.edicao'),
    url(r'^checklist/relatorio/pdf/', 'restrito.checklist.relatorio_pdf'),
    url(r'^checklist/relatorio/ods/', 'restrito.checklist.relatorio_ods'),
    url(r'^checklist/relatorio/csv/', 'restrito.checklist.relatorio_csv'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sub_area/consulta/', 'restrito.sub_area.consulta'),
    url(r'^sub_area/cadastro/', 'restrito.sub_area.cadastro'),
    url(r'^sub_area/edicao/(?P<id>\d+)/', 'restrito.sub_area.edicao'),

    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^tipo_caixa/consulta/', 'restrito.tipo_caixa.consulta'),
    url(r'^tipo_caixa/cadastro/', 'restrito.tipo_caixa.cadastro'),
    url(r'^tipo_caixa/edicao/(?P<id>\d+)/', 'restrito.tipo_caixa.edicao'),
    
    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^tipo_processo/consulta/', 'restrito.tipo_processo.consulta'),
    url(r'^tipo_processo/cadastro/', 'restrito.tipo_processo.cadastro'),
    url(r'^tipo_processo/edicao/(?P<id>\d+)/', 'restrito.tipo_processo.edicao'),
    url(r'^tipo_processo/relatorio/pdf/', 'restrito.tipo_processo.relatorio_pdf'),
    url(r'^tipo_processo/relatorio/ods/', 'restrito.tipo_processo.relatorio_ods'),
    url(r'^tipo_processo/relatorio/csv/', 'restrito.tipo_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^tipo_pendencia/consulta/', 'restrito.tipo_pendencia.consulta'),
    url(r'^tipo_pendencia/cadastro/', 'restrito.tipo_pendencia.cadastro'),
    url(r'^tipo_pendencia/edicao/(?P<id>\d+)/', 'restrito.tipo_pendencia.edicao'),
    url(r'^tipo_pendencia/relatorio/pdf/', 'restrito.tipo_pendencia.relatorio_pdf'),
    url(r'^tipo_pendencia/relatorio/ods/', 'restrito.tipo_pendencia.relatorio_ods'),
    url(r'^tipo_pendencia/relatorio/csv/', 'restrito.tipo_pendencia.relatorio_csv'),

    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^processo/consulta/', 'restrito.processo.consulta'),   
    url(r'^processo/cadastro/', 'restrito.processo.cadastro'),
    url(r'^processo/edicao/(?P<id>\d+)/', 'restrito.processo.edicao'),
    url(r'^processo/tramitacao/(?P<base>\d+)/', 'restrito.processo.tramitar'),
    url(r'^processo/tramitacao_massa/', 'restrito.processo.ativar_tramitacao_massa'),
    url(r'^processo/add_tramitacao_massa/(?P<base>\d+)/', 'restrito.processo.add_tramitacao_massa'),
    url(r'^processo/rem_tramitacao_massa/(?P<base>\d+)/', 'restrito.processo.rem_tramitacao_massa'),
    url(r'^processo/lista_tramitacao_massa/', 'restrito.processo.executar_tramitacao_massa'),
    url(r'^processo/anexo/(?P<base>\d+)/', 'restrito.processo.anexar'),
    url(r'^processo/pendencia/(?P<base>\d+)/', 'restrito.processo.criar_pendencia'),   
    url(r'^processo/relatorio/pdf/', 'restrito.processo.relatorio_pdf'),   
    url(r'^processo/relatorio/ods/', 'restrito.processo.relatorio_ods'),
    url(r'^processo/relatorio/csv/', 'restrito.processo.relatorio_csv'),
    url(r'^processo/desanexar/(?P<id_anexo>\d+)/', 'restrito.processo.desanexar'),
    url(r'^processo/consultaProcesso/', 'restrito.processo.consultaprocesso'),   
   
    # ACESSO RESTRITO SICOP PENDENCIA
    url(r'^pendencia/edicao/(?P<pendencia>\d+)/', 'restrito.pendencia.edicao'),

    # IMPORTACAO DE PROCESSOS ATRAVES DE PLANILHA ODS
    url(r'^processo/importacao/', 'restrito.processo.importacao_ods'),

    # EXPORTACAO SQLITE
    url(r'^android/exportacao/', 'util.app_android.gerar_sqlite'),
    
    # PROCESSO RURAL
    url(r'^processo/rural/consulta/', 'restrito.processo_rural.consulta'),
    url(r'^processo/rural/cadastro/', 'restrito.processo_rural.cadastro'),
    url(r'^processo/rural/edicao/(?P<id>\d+)/', 'restrito.processo_rural.edicao'),
    url(r'^processo/rural/sobreposicao/(?P<id>\d+)/', 'restrito.processo_rural.gerar_doc_sobreposicao'),
    url(r'^processo/rural/despacho_aprovacao_regional/(?P<id>\d+)/', 'restrito.processo_rural.gerar_doc_despacho_aprovacao_regional'),
    # PROCESSO URBANO
    url(r'^processo/urbano/consulta/', 'restrito.processo_urbano.consulta'),
    url(r'^processo/urbano/cadastro/', 'restrito.processo_urbano.cadastro'),
    url(r'^processo/urbano/edicao/(?P<id>\d+)/', 'restrito.processo_urbano.edicao'),
    # PROCESSO CLAUSULA RESOLUTIVA
    url(r'^processo/clausula/analise/', 'restrito.processo_clausula.analise'),
    url(r'^processo/clausula/programacao_p80/', 'restrito.processo_clausula.programacao_p80'),
    url(r'^processo/clausula/notificacao/', 'restrito.processo_clausula.notificacao'),
    url(r'^processo/clausula/consulta/', 'restrito.processo_clausula.consulta'),
    url(r'^processo/clausula/cadastro/', 'restrito.processo_clausula.cadastro'),
    url(r'^processo/clausula/edicao/(?P<id>\d+)/', 'restrito.processo_clausula.edicao'),   
    
   # ACESSO RESTRITO SICOP PECA TECNICA 
    url(r'^peca_tecnica/consulta/', 'restrito.peca_tecnica.consulta'),
    url(r'^peca_tecnica/cadastro/', 'restrito.peca_tecnica.cadastro'),
    url(r'^peca_tecnica/edicao/(?P<id>\d+)/', 'restrito.peca_tecnica.edicao'),
    url(r'^peca_tecnica/relatorio/pdf/', 'restrito.peca_tecnica.relatorio_pdf'),
    url(r'^peca_tecnica/relatorio/ods/', 'restrito.peca_tecnica.relatorio_ods'),
    url(r'^peca_tecnica/relatorio/csv/', 'restrito.peca_tecnica.relatorio_csv'),
            
    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^situacao_processo/consulta/', 'restrito.situacao_processo.consulta'),
    url(r'^situacao_processo/cadastro/', 'restrito.situacao_processo.cadastro'),
    url(r'^situacao_processo/edicao/(?P<id>\d+)/', 'restrito.situacao_processo.edicao'),
    url(r'^situacao_processo/relatorio/pdf/', 'restrito.situacao_processo.relatorio_pdf'),
    url(r'^situacao_processo/relatorio/ods/', 'restrito.situacao_processo.relatorio_ods'),
    url(r'^situacao_processo/relatorio/csv/', 'restrito.situacao_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^situacao_geo/consulta/', 'restrito.situacao_geo.consulta'),
    url(r'^situacao_geo/cadastro/', 'restrito.situacao_geo.cadastro'),
    url(r'^situacao_geo/edicao/(?P<id>\d+)/', 'restrito.situacao_geo.edicao'),
    url(r'^situacao_geo/relatorio/pdf/', 'restrito.situacao_geo.relatorio_pdf'),
    url(r'^situacao_geo/relatorio/ods/', 'restrito.situacao_geo.relatorio_ods'),
    url(r'^situacao_geo/relatorio/csv/', 'restrito.situacao_geo.relatorio_csv'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^classificacao_processo/consulta/', 'restrito.classificacao_processo.consulta'),
    url(r'^classificacao_processo/cadastro/', 'restrito.classificacao_processo.cadastro'),
    url(r'^classificacao_processo/edicao/(?P<id>\d+)/', 'restrito.classificacao_processo.edicao'),
    url(r'^classificacao_processo/relatorio/pdf/', 'restrito.classificacao_processo.relatorio_pdf'),
    url(r'^classificacao_processo/relatorio/ods/', 'restrito.classificacao_processo.relatorio_ods'),
    url(r'^classificacao_processo/relatorio/csv/', 'restrito.classificacao_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^status_pendencia/consulta/', 'restrito.status_pendencia.consulta'),
    url(r'^status_pendencia/cadastro/', 'restrito.status_pendencia.cadastro'),
    url(r'^status_pendencia/edicao/(?P<id>\d+)/', 'restrito.status_pendencia.edicao'),
    url(r'^status_pendencia/relatorio/pdf/', 'restrito.status_pendencia.relatorio_pdf'),
    url(r'^status_pendencia/relatorio/ods/', 'restrito.status_pendencia.relatorio_ods'),
    url(r'^status_pendencia/relatorio/csv/', 'restrito.status_pendencia.relatorio_csv'),

   # ACESSO RESTRITO SICOP DIVISAO
    url(r'^divisao/consulta/', 'restrito.divisao.consulta'),
    url(r'^divisao/cadastro/', 'restrito.divisao.cadastro'),
    url(r'^divisao/edicao/(?P<id>\d+)/', 'restrito.divisao.edicao'),
    url(r'^divisao/relatorio/pdf/', 'restrito.divisao.relatorio_pdf'),
    url(r'^divisao/relatorio/ods/', 'restrito.divisao.relatorio_ods'),
    url(r'^divisao/relatorio/csv/', 'restrito.divisao.relatorio_csv'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^grupo/consulta/', 'restrito.grupo.consulta'),
    url(r'^grupo/cadastro/', 'restrito.grupo.cadastro'),
    url(r'^grupo/edicao/(?P<id>\d+)/', 'restrito.grupo.edicao'),
    url(r'^grupo/relatorio/pdf/', 'restrito.grupo.relatorio_pdf'),
    url(r'^grupo/relatorio/ods/', 'restrito.grupo.relatorio_ods'),
    url(r'^grupo/relatorio/csv/', 'restrito.grupo.relatorio_csv'),

  # ACESSO RESTRITO SICOP PERMISSAO
    url(r'^permissao/consulta/', 'restrito.permissao.consulta'),
    url(r'^permissao/cadastro/', 'restrito.permissao.cadastro'),
    url(r'^permissao/edicao/(?P<id>\d+)/', 'restrito.permissao.edicao'),
    url(r'^permissao/relatorio/pdf/', 'restrito.permissao.relatorio_pdf'),
    url(r'^permissao/relatorio/ods/', 'restrito.permissao.relatorio_ods'),
    url(r'^permissao/relatorio/csv/', 'restrito.permissao.relatorio_csv'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^usuario/consulta/', 'restrito.usuario.consulta'),
    url(r'^usuario/cadastro/', 'restrito.usuario.cadastro'),
    url(r'^usuario/edicao/(?P<id>\d+)/', 'restrito.usuario.edicao'),
    url(r'^usuario/edicao/usuario/(?P<id>\d+)/', 'restrito.usuario.edicao_usuario_logado'),
    url(r'^usuario/relatorio/pdf/', 'restrito.usuario.relatorio_pdf'),
    url(r'^usuario/relatorio/ods/', 'restrito.usuario.relatorio_ods'),
    url(r'^usuario/relatorio/csv/', 'restrito.usuario.relatorio_csv'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    
    url(r'^municipio/consulta/', 'restrito.municipio.consulta'),
    url(r'^municipio/edicao/(?P<id>\d+)/', 'restrito.municipio.edicao'),
   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^relatorio/lista/', 'restrito.relatorio.lista'),
    url(r'^relatorio/processos/', 'restrito.relatorio.processos'),
    url(r'^relatorio/varredura_processos/', 'restrito.relatorio.varredura_processos'),
    url(r'^relatorio/processo_peca/', 'restrito.relatorio.processo_peca'),
    url(r'^relatorio/processo_sem_peca/', 'restrito.relatorio.processo_sem_peca'),
    url(r'^relatorio/processo_sem_peca_com_parcela_sigef/', 'restrito.relatorio.processo_sem_peca_com_parcela_sigef'),
    url(r'^relatorio/peca_processo/', 'restrito.relatorio.peca_processo'),
    url(r'^relatorio/peca_gleba/', 'restrito.relatorio.peca_gleba'),
    url(r'^relatorio/peca_nao_aprovada/', 'restrito.relatorio.peca_nao_aprovada'),
    url(r'^relatorio/peca_rejeitada/', 'restrito.relatorio.peca_rejeitada'),
    url(r'^relatorio/peca_sem_processo/', 'restrito.relatorio.peca_sem_processo'),
    url(r'^relatorio/peca_validada/', 'restrito.relatorio.peca_validada'),
    url(r'^relatorio/peca/', 'restrito.relatorio.pecas'),

    #ACESSO RESTRITO SICOP RELATORIO SIGEF
    url(r'^relatorio/processo_parcela/', 'restrito.relatorio.processo_parcela'),
    url(r'^relatorio/processo_sem_parcela/', 'restrito.relatorio.processo_sem_parcela'),
    url(r'^relatorio/parcela_processo/', 'restrito.relatorio.parcela_processo'),
    url(r'^relatorio/parcela_sem_processo/', 'restrito.relatorio.parcela_sem_processo'),
        
    #ACESSO RESTRITO SICOP FLUXO
    url(r'^relatorio/etapa/p23/', 'restrito.relatorio.etapa_p23'),
    url(r'^relatorio/etapa/p80/', 'restrito.relatorio.etapa_p80'),
    url(r'^relatorio/etapa/urbano/', 'restrito.relatorio.etapa_urbano'),
    
    url(r'^relatorio/programacao_p80/', 'restrito.relatorio.em_programacao_p80'),
    url(r'^relatorio/prazos_notificacoes_p80/', 'restrito.relatorio.prazos_notificacoes_p80'),
    url(r'^relatorio/titulo/', 'restrito.relatorio.titulos'),
    
    #END------------------------------SICOP---------------------------------------------------------------------------------
   
    # ACESSO RESTRITO TABELA SITUACAO 
    url(r'^situacao/consulta/', 'restrito.situacao.consulta'),
    url(r'^situacao/edicao/(?P<id>\d+)/','restrito.situacao.edicao'),
    url(r'^situacao/cadastro/', 'restrito.situacao.cadastro'),
    #END------------------------------CONTROLE---------------------------------------------------------------------------------

    url(r'^processamento/', 'admin.processamento'),

   )
