# coding: utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('TerraLegal.documento',
    url(r'^tipo/consulta/', 'tipo_documento.consulta'),   
    url(r'^tipo/cadastro/', 'tipo_documento.cadastro'),
    url(r'^tipo/edicao/(?P<id>\d+)/', 'tipo_documento.edicao'),

    url(r'^tipo/relatorio/pdf/', 'tipo_documento.relatorio_pdf'),
    url(r'^tipo/relatorio/ods/', 'tipo_documento.relatorio_ods'),
    url(r'^tipo/relatorio/csv/', 'tipo_documento.relatorio_csv'),

    url(r'^consulta/', 'documento.consulta'),   
    url(r'^cadastro/', 'documento.cadastro'),
    url(r'^edicao/(?P<id>\d+)/', 'documento.edicao'),

    # DOCUMENTO MEMORANDO
    url(r'^memorando/consulta/', 'documento_memorando.consulta'),
    url(r'^memorando/cadastro/', 'documento_memorando.cadastro'),
    url(r'^memorando/edicao/(?P<id>\d+)/', 'documento_memorando.edicao'),
    url(r'^memorando/criacao/(?P<id>\d+)/', 'documento_memorando.criacao'),

    # DOCUMENTO OFICIO
    url(r'^oficio/consulta/', 'documento_oficio.consulta'),
    url(r'^oficio/cadastro/', 'documento_oficio.cadastro'),
    url(r'^oficio/edicao/(?P<id>\d+)/', 'documento_oficio.edicao'),
    url(r'^oficio/criacao/(?P<id>\d+)/', 'documento_oficio.criacao'),
    
    # DOCUMENTO REQUISICAO DE VIATURA
    url(r'^requisicao_viatura/consulta/', 'documento_requisicao_viatura.consulta'),
    url(r'^requisicao_viatura/cadastro/', 'documento_requisicao_viatura.cadastro'),
    url(r'^requisicao_viatura/edicao/(?P<id>\d+)/', 'documento_requisicao_viatura.edicao'),
    url(r'^requisicao_viatura/criacao/(?P<id>\d+)/', 'documento_requisicao_viatura.criacao'),
    
    # DOCUMENTO RME
    url(r'^rme/consulta/', 'documento_rme.consulta'),
    url(r'^rme/cadastro/', 'documento_rme.cadastro'),
    url(r'^rme/edicao/(?P<id>\d+)/', 'documento_rme.edicao'),
    url(r'^rme/criacao/(?P<id>\d+)/', 'documento_rme.criacao'),
    url(r'^rme/material/(?P<doc>\d+)/', 'documento_rme.criar_material'),
    url(r'^rme/material/edicao/(?P<materialrme>\d+)/', 'materialrme.edicao'),

   )
   
