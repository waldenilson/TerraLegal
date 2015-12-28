# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
project = 'project'

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
    url(r'^geoinformacao/',include(project+'.geoinformacao.urls',namespace='geoinformacao')),
    url(r'^tramitacao/',include(project+'.tramitacao.urls',namespace='tramitacao')),


    # ACESSO AO PUBLICO
    url(r'^$', project+'.web.views_publicas.inicio'),
    url(r'^web/estatisticas/', project+'.web.estatisticas.estatisticas'),
    url(r'^web/mobile/', project+'.web.views_publicas.mobile'),
    url(r'^media/(?P<path>.*)$',project+'.tramitacao.util.media.download', {'document_root': settings.MEDIA_ROOT}),
   
    # GEOINFORMACOES
    url(r'^geo/glebas_federais/', project+'.tramitacao.restrito.geoinformacao.glebas_federais'),
    url(r'^geo/openlayers/', project+'.tramitacao.restrito.geoinformacao.openlayers'),
    
    #INIT------------------------------SICOP---------------------------------------------------------------------------------

    # ACESSO RESTRITO SICOP PROCESSO
            
    # ESCOLHA DO TIPO DE PROCESSO
    url(r'^sicop/processo/consulta/', project+'.tramitacao.restrito.processo.consulta'),   
    url(r'^sicop/processo/cadastro/', project+'.tramitacao.restrito.processo.cadastro'),
    url(r'^sicop/processo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.processo.edicao'),
    url(r'^sicop/processo/tramitacao/(?P<base>\d+)/', project+'.tramitacao.restrito.processo.tramitar'),
    url(r'^sicop/processo/tramitacao_massa/', project+'.tramitacao.restrito.processo.ativar_tramitacao_massa'),
    url(r'^sicop/processo/add_tramitacao_massa/(?P<base>\d+)/', project+'.tramitacao.restrito.processo.add_tramitacao_massa'),
    url(r'^sicop/processo/rem_tramitacao_massa/(?P<base>\d+)/', project+'.tramitacao.restrito.processo.rem_tramitacao_massa'),
    url(r'^sicop/processo/lista_tramitacao_massa/', project+'.tramitacao.restrito.processo.executar_tramitacao_massa'),
    url(r'^sicop/processo/anexo/(?P<base>\d+)/', project+'.tramitacao.restrito.processo.anexar'),
    url(r'^sicop/processo/pendencia/(?P<base>\d+)/', project+'.tramitacao.restrito.processo.criar_pendencia'),   
    url(r'^sicop/processo/relatorio/pdf/', project+'.tramitacao.restrito.processo.relatorio_pdf'),   
    url(r'^sicop/processo/relatorio/ods/', project+'.tramitacao.restrito.processo.relatorio_ods'),
    url(r'^sicop/processo/relatorio/csv/', project+'.tramitacao.restrito.processo.relatorio_csv'),
    url(r'^sicop/processo/desanexar/(?P<id_anexo>\d+)/', project+'.tramitacao.restrito.processo.desanexar'),
    url(r'^sicop/processo/consultaProcesso/', project+'.tramitacao.restrito.processo.consultaprocesso'),   
   
    # ACESSO RESTRITO SICOP PENDENCIA
    url(r'^sicop/pendencia/edicao/(?P<pendencia>\d+)/', project+'.tramitacao.restrito.pendencia.edicao'),

    # IMPORTACAO DE PROCESSOS ATRAVES DE PLANILHA ODS
    url(r'^sicop/processo/importacao/', project+'.tramitacao.restrito.processo.importacao_ods'),
    
    # PROCESSO RURAL
    url(r'^sicop/processo/rural/consulta/', project+'.tramitacao.restrito.processo_rural.consulta'),
    url(r'^sicop/processo/rural/cadastro/', project+'.tramitacao.restrito.processo_rural.cadastro'),
    url(r'^sicop/processo/rural/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.processo_rural.edicao'),
    url(r'^sicop/processo/rural/sobreposicao/(?P<id>\d+)/', project+'.tramitacao.restrito.processo_rural.gerar_doc_sobreposicao'),
    url(r'^sicop/processo/rural/despacho_aprovacao_regional/(?P<id>\d+)/', project+'.tramitacao.restrito.processo_rural.gerar_doc_despacho_aprovacao_regional'),
    # PROCESSO URBANO
    url(r'^sicop/processo/urbano/consulta/', project+'.tramitacao.restrito.processo_urbano.consulta'),
    url(r'^sicop/processo/urbano/cadastro/', project+'.tramitacao.restrito.processo_urbano.cadastro'),
    url(r'^sicop/processo/urbano/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.processo_urbano.edicao'),
    # PROCESSO CLAUSULA RESOLUTIVA
    url(r'^sicop/processo/clausula/analise/', project+'.tramitacao.restrito.processo_clausula.analise'),
    url(r'^sicop/processo/clausula/programacao_p80/', project+'.tramitacao.restrito.processo_clausula.programacao_p80'),
    url(r'^sicop/processo/clausula/notificacao/', project+'.tramitacao.restrito.processo_clausula.notificacao'),
    url(r'^sicop/processo/clausula/consulta/', project+'.tramitacao.restrito.processo_clausula.consulta'),
    url(r'^sicop/processo/clausula/cadastro/', project+'.tramitacao.restrito.processo_clausula.cadastro'),
    url(r'^sicop/processo/clausula/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.processo_clausula.edicao'),   
    
   # ACESSO RESTRITO SICOP PECA TECNICA 
    url(r'^sicop/peca_tecnica/consulta/', project+'.tramitacao.restrito.peca_tecnica.consulta'),
    url(r'^sicop/peca_tecnica/cadastro/', project+'.tramitacao.restrito.peca_tecnica.cadastro'),
    url(r'^sicop/peca_tecnica/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.peca_tecnica.edicao'),
    url(r'^sicop/peca_tecnica/relatorio/pdf/', project+'.tramitacao.restrito.peca_tecnica.relatorio_pdf'),
    url(r'^sicop/peca_tecnica/relatorio/ods/', project+'.tramitacao.restrito.peca_tecnica.relatorio_ods'),
    url(r'^sicop/peca_tecnica/relatorio/csv/', project+'.tramitacao.restrito.peca_tecnica.relatorio_csv'),
    
   # ACESSO RESTRITO SICOP PREGAO 
    url(r'^sicop/pregao/consulta/', project+'.tramitacao.restrito.pregao.consulta'),
    url(r'^sicop/pregao/cadastro/', project+'.tramitacao.restrito.pregao.cadastro'),
    url(r'^sicop/pregao/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.pregao.edicao'),
    
    # ACESSO RESTRITO SICOP GLEBA
    url(r'^sicop/gleba/consulta/', project+'.tramitacao.restrito.gleba.consulta'),
    url(r'^sicop/gleba/cadastro/', project+'.tramitacao.restrito.gleba.cadastro'),
    url(r'^sicop/gleba/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.gleba.edicao'),
    
    # ACESSO RESTRITO SICOP CAIXA
    url(r'^sicop/caixa/consulta/', project+'.tramitacao.restrito.caixa.consulta'),
    url(r'^sicop/caixa/cadastro/', project+'.tramitacao.restrito.caixa.cadastro'),
    url(r'^sicop/caixa/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.caixa.edicao'),
    url(r'^sicop/caixa/relatorio/pdf/', project+'.tramitacao.restrito.caixa.relatorio_pdf'),
    url(r'^sicop/caixa/relatorio/ods/', project+'.tramitacao.restrito.caixa.relatorio_ods'),
    url(r'^sicop/caixa/relatorio/titulo/ods/', project+'.tramitacao.restrito.caixa.relatorio_titulo_ods'),
    url(r'^sicop/caixa/relatorio/csv/', project+'.tramitacao.restrito.caixa.relatorio_csv'),

    # ACESSO RESTRITO SICOP ETAPA
    url(r'^sicop/etapa/consulta/', project+'.tramitacao.restrito.etapa.consulta'),
    url(r'^sicop/etapa/cadastro/', project+'.tramitacao.restrito.etapa.cadastro'),
    url(r'^sicop/etapa/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.etapa.edicao'),
    url(r'^sicop/etapa/relatorio/pdf/', project+'.tramitacao.restrito.etapa.relatorio_pdf'),
    url(r'^sicop/etapa/relatorio/ods/', project+'.tramitacao.restrito.etapa.relatorio_ods'),
    url(r'^sicop/etapa/relatorio/csv/', project+'.tramitacao.restrito.etapa.relatorio_csv'),
    url(r'^sicop/etapa/checklist/(?P<processo>\d+)/(?P<etapa>\d+)/', project+'.tramitacao.restrito.etapa.checklist'),
    url(r'^sicop/etapa/restaurar/(?P<processo>\d+)/', project+'.tramitacao.restrito.etapa.restaurar'),

    # ACESSO RESTRITO SICOP CHECKLIST
    url(r'^sicop/checklist/consulta/', project+'.tramitacao.restrito.checklist.consulta'),
    url(r'^sicop/checklist/cadastro/', project+'.tramitacao.restrito.checklist.cadastro'),
    url(r'^sicop/checklist/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.checklist.edicao'),
    url(r'^sicop/checklist/relatorio/pdf/', project+'.tramitacao.restrito.checklist.relatorio_pdf'),
    url(r'^sicop/checklist/relatorio/ods/', project+'.tramitacao.restrito.checklist.relatorio_ods'),
    url(r'^sicop/checklist/relatorio/csv/', project+'.tramitacao.restrito.checklist.relatorio_csv'),

    # ACESSO RESTRITO SICOP SUBAREA
    url(r'^sicop/sub_area/consulta/', project+'.tramitacao.restrito.sub_area.consulta'),
    url(r'^sicop/sub_area/cadastro/', project+'.tramitacao.restrito.sub_area.cadastro'),
    url(r'^sicop/sub_area/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.sub_area.edicao'),
    
    # ACESSO RESTRITO SICOP TIPO CAIXA
    url(r'^sicop/tipo_caixa/consulta/', project+'.tramitacao.restrito.tipo_caixa.consulta'),
    url(r'^sicop/tipo_caixa/cadastro/', project+'.tramitacao.restrito.tipo_caixa.cadastro'),
    url(r'^sicop/tipo_caixa/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.tipo_caixa.edicao'),
    
    # ACESSO RESTRITO SICOP TIPO PROCESSO
    url(r'^sicop/tipo_processo/consulta/', project+'.tramitacao.restrito.tipo_processo.consulta'),
    url(r'^sicop/tipo_processo/cadastro/', project+'.tramitacao.restrito.tipo_processo.cadastro'),
    url(r'^sicop/tipo_processo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.tipo_processo.edicao'),
    url(r'^sicop/tipo_processo/relatorio/pdf/', project+'.tramitacao.restrito.tipo_processo.relatorio_pdf'),
    url(r'^sicop/tipo_processo/relatorio/ods/', project+'.tramitacao.restrito.tipo_processo.relatorio_ods'),
    url(r'^sicop/tipo_processo/relatorio/csv/', project+'.tramitacao.restrito.tipo_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP TIPO PENDENCIA
    url(r'^sicop/tipo_pendencia/consulta/', project+'.tramitacao.restrito.tipo_pendencia.consulta'),
    url(r'^sicop/tipo_pendencia/cadastro/', project+'.tramitacao.restrito.tipo_pendencia.cadastro'),
    url(r'^sicop/tipo_pendencia/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.tipo_pendencia.edicao'),
    url(r'^sicop/tipo_pendencia/relatorio/pdf/', project+'.tramitacao.restrito.tipo_pendencia.relatorio_pdf'),
    url(r'^sicop/tipo_pendencia/relatorio/ods/', project+'.tramitacao.restrito.tipo_pendencia.relatorio_ods'),
    url(r'^sicop/tipo_pendencia/relatorio/csv/', project+'.tramitacao.restrito.tipo_pendencia.relatorio_csv'),

    # ACESSO RESTRITO SICOP SITUACAO PROCESSO
    url(r'^sicop/situacao_processo/consulta/', project+'.tramitacao.restrito.situacao_processo.consulta'),
    url(r'^sicop/situacao_processo/cadastro/', project+'.tramitacao.restrito.situacao_processo.cadastro'),
    url(r'^sicop/situacao_processo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.situacao_processo.edicao'),
    url(r'^sicop/situacao_processo/relatorio/pdf/', project+'.tramitacao.restrito.situacao_processo.relatorio_pdf'),
    url(r'^sicop/situacao_processo/relatorio/ods/', project+'.tramitacao.restrito.situacao_processo.relatorio_ods'),
    url(r'^sicop/situacao_processo/relatorio/csv/', project+'.tramitacao.restrito.situacao_processo.relatorio_csv'),


    # ACESSO RESTRITO SICOP SITUACAO GEO
    url(r'^sicop/situacao_geo/consulta/', project+'.tramitacao.restrito.situacao_geo.consulta'),
    url(r'^sicop/situacao_geo/cadastro/', project+'.tramitacao.restrito.situacao_geo.cadastro'),
    url(r'^sicop/situacao_geo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.situacao_geo.edicao'),
    url(r'^sicop/situacao_geo/relatorio/pdf/', project+'.tramitacao.restrito.situacao_geo.relatorio_pdf'),
    url(r'^sicop/situacao_geo/relatorio/ods/', project+'.tramitacao.restrito.situacao_geo.relatorio_ods'),
    url(r'^sicop/situacao_geo/relatorio/csv/', project+'.tramitacao.restrito.situacao_geo.relatorio_csv'),

    # ACESSO RESTRITO SICOP CLASSIFICACAO PROCESSO
    url(r'^sicop/classificacao_processo/consulta/', project+'.tramitacao.restrito.classificacao_processo.consulta'),
    url(r'^sicop/classificacao_processo/cadastro/', project+'.tramitacao.restrito.classificacao_processo.cadastro'),
    url(r'^sicop/classificacao_processo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.classificacao_processo.edicao'),
    url(r'^sicop/classificacao_processo/relatorio/pdf/', project+'.tramitacao.restrito.classificacao_processo.relatorio_pdf'),
    url(r'^sicop/classificacao_processo/relatorio/ods/', project+'.tramitacao.restrito.classificacao_processo.relatorio_ods'),
    url(r'^sicop/classificacao_processo/relatorio/csv/', project+'.tramitacao.restrito.classificacao_processo.relatorio_csv'),

    # ACESSO RESTRITO SICOP STATUS PENDENCIA
    url(r'^sicop/status_pendencia/consulta/', project+'.tramitacao.restrito.status_pendencia.consulta'),
    url(r'^sicop/status_pendencia/cadastro/', project+'.tramitacao.restrito.status_pendencia.cadastro'),
    url(r'^sicop/status_pendencia/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.status_pendencia.edicao'),
    url(r'^sicop/status_pendencia/relatorio/pdf/', project+'.tramitacao.restrito.status_pendencia.relatorio_pdf'),
    url(r'^sicop/status_pendencia/relatorio/ods/', project+'.tramitacao.restrito.status_pendencia.relatorio_ods'),
    url(r'^sicop/status_pendencia/relatorio/csv/', project+'.tramitacao.restrito.status_pendencia.relatorio_csv'),

   # ACESSO RESTRITO SICOP DIVISAO
    url(r'^sicop/divisao/consulta/', project+'.tramitacao.restrito.divisao.consulta'),
    url(r'^sicop/divisao/cadastro/', project+'.tramitacao.restrito.divisao.cadastro'),
    url(r'^sicop/divisao/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.divisao.edicao'),
    url(r'^sicop/divisao/relatorio/pdf/', project+'.tramitacao.restrito.divisao.relatorio_pdf'),
    url(r'^sicop/divisao/relatorio/ods/', project+'.tramitacao.restrito.divisao.relatorio_ods'),
    url(r'^sicop/divisao/relatorio/csv/', project+'.tramitacao.restrito.divisao.relatorio_csv'),
  
  # ACESSO RESTRITO SICOP GRUPO
    url(r'^sicop/grupo/consulta/', project+'.tramitacao.restrito.grupo.consulta'),
    url(r'^sicop/grupo/cadastro/', project+'.tramitacao.restrito.grupo.cadastro'),
    url(r'^sicop/grupo/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.grupo.edicao'),
    url(r'^sicop/grupo/relatorio/pdf/', project+'.tramitacao.restrito.grupo.relatorio_pdf'),
    url(r'^sicop/grupo/relatorio/ods/', project+'.tramitacao.restrito.grupo.relatorio_ods'),
    url(r'^sicop/grupo/relatorio/csv/', project+'.tramitacao.restrito.grupo.relatorio_csv'),

  # ACESSO RESTRITO SICOP PERMISSAO
    url(r'^sicop/permissao/consulta/', project+'.tramitacao.restrito.permissao.consulta'),
    url(r'^sicop/permissao/cadastro/', project+'.tramitacao.restrito.permissao.cadastro'),
    url(r'^sicop/permissao/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.permissao.edicao'),
    url(r'^sicop/permissao/relatorio/pdf/', project+'.tramitacao.restrito.permissao.relatorio_pdf'),
    url(r'^sicop/permissao/relatorio/ods/', project+'.tramitacao.restrito.permissao.relatorio_ods'),
    url(r'^sicop/permissao/relatorio/csv/', project+'.tramitacao.restrito.permissao.relatorio_csv'),

  # ACESSO RESTRITO SICOP USUARIO
    url(r'^sicop/usuario/consulta/', project+'.tramitacao.restrito.usuario.consulta'),
    url(r'^sicop/usuario/cadastro/', project+'.tramitacao.restrito.usuario.cadastro'),
    url(r'^sicop/usuario/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.usuario.edicao'),
    url(r'^sicop/usuario/edicao/usuario/(?P<id>\d+)/', project+'.tramitacao.restrito.usuario.edicao_usuario_logado'),
    url(r'^sicop/usuario/relatorio/pdf/', project+'.tramitacao.restrito.usuario.relatorio_pdf'),
    url(r'^sicop/usuario/relatorio/ods/', project+'.tramitacao.restrito.usuario.relatorio_ods'),
    url(r'^sicop/usuario/relatorio/csv/', project+'.tramitacao.restrito.usuario.relatorio_csv'),

    # ACESSO RESTRITO SICOP MUNICIPIO
    
    url(r'^sicop/municipio/consulta/', project+'.tramitacao.restrito.municipio.consulta'),
    url(r'^sicop/municipio/edicao/(?P<id>\d+)/', project+'.tramitacao.restrito.municipio.edicao'),
   
    # ACESSO RESTRITO SICOP RELATORIO
    url(r'^sicop/relatorio/lista/', project+'.tramitacao.restrito.relatorio.lista'),
    url(r'^sicop/relatorio/processos/', project+'.tramitacao.restrito.relatorio.processos'),
    url(r'^sicop/relatorio/varredura_processos/', project+'.tramitacao.restrito.relatorio.varredura_processos'),
    url(r'^sicop/relatorio/processo_peca/', project+'.tramitacao.restrito.relatorio.processo_peca'),
    url(r'^sicop/relatorio/processo_sem_peca/', project+'.tramitacao.restrito.relatorio.processo_sem_peca'),
    url(r'^sicop/relatorio/processo_sem_peca_com_parcela_sigef/', project+'.tramitacao.restrito.relatorio.processo_sem_peca_com_parcela_sigef'),
    url(r'^sicop/relatorio/peca_processo/', project+'.tramitacao.restrito.relatorio.peca_processo'),
    url(r'^sicop/relatorio/peca_gleba/', project+'.tramitacao.restrito.relatorio.peca_gleba'),
    url(r'^sicop/relatorio/peca_nao_aprovada/', project+'.tramitacao.restrito.relatorio.peca_nao_aprovada'),
    url(r'^sicop/relatorio/peca_rejeitada/', project+'.tramitacao.restrito.relatorio.peca_rejeitada'),
    url(r'^sicop/relatorio/peca_sem_processo/', project+'.tramitacao.restrito.relatorio.peca_sem_processo'),
    url(r'^sicop/relatorio/peca_validada/', project+'.tramitacao.restrito.relatorio.peca_validada'),
    url(r'^sicop/relatorio/peca/', project+'.tramitacao.restrito.relatorio.pecas'),

    #ACESSO RESTRITO SICOP RELATORIO SIGEF
    url(r'^sicop/relatorio/processo_parcela/', project+'.tramitacao.restrito.relatorio.processo_parcela'),
    url(r'^sicop/relatorio/processo_sem_parcela/', project+'.tramitacao.restrito.relatorio.processo_sem_parcela'),
    url(r'^sicop/relatorio/parcela_processo/', project+'.tramitacao.restrito.relatorio.parcela_processo'),
    url(r'^sicop/relatorio/parcela_sem_processo/', project+'.tramitacao.restrito.relatorio.parcela_sem_processo'),
        
    #ACESSO RESTRITO SICOP FLUXO
    url(r'^sicop/relatorio/etapa/p23/', project+'.tramitacao.restrito.relatorio.etapa_p23'),
    url(r'^sicop/relatorio/etapa/p80/', project+'.tramitacao.restrito.relatorio.etapa_p80'),
    url(r'^sicop/relatorio/etapa/urbano/', project+'.tramitacao.restrito.relatorio.etapa_urbano'),
    
    url(r'^sicop/relatorio/programacao_p80/', project+'.tramitacao.restrito.relatorio.em_programacao_p80'),
    url(r'^sicop/relatorio/prazos_notificacoes_p80/', project+'.tramitacao.restrito.relatorio.prazos_notificacoes_p80'),
    url(r'^sicop/relatorio/titulo/', project+'.tramitacao.restrito.relatorio.titulos'),
    
    #END------------------------------SICOP---------------------------------------------------------------------------------
   
    # ACESSO RESTRITO TABELA SITUACAO 
    url(r'^sicop/situacao/consulta/', project+'.tramitacao.restrito.situacao.consulta'),
    url(r'^sicop/situacao/edicao/(?P<id>\d+)/',project+'.tramitacao.restrito.situacao.edicao'),
    url(r'^sicop/situacao/cadastro/', project+'.tramitacao.restrito.situacao.cadastro'),
    #END------------------------------CONTROLE---------------------------------------------------------------------------------

    url(r'^sicop/processamento/', project+'.tramitacao.admin.processamento'),
        
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    url(r'^sicop/admin/', include(admin.site.urls)),
    
)
