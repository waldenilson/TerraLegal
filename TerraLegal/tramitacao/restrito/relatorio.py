# -*- coding: UTF-8 -*-
from django.template.context import RequestContext
from TerraLegal.tramitacao.models import Tbpecastecnicas, \
    Tbprocessorural,Tbchecklistprocessobase, Tbprocessosanexos, Tbprocessobase,Tbprocessourbano, Tbcaixa, AuthUser, Tbmunicipio, Tbprocessoclausula, Tbpendencia, Tbetapa, Tbtransicao
from TerraLegal.tramitacao.relatorio_base import relatorio_ods_base_header,\
    relatorio_ods_base
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponse
from odslib import ODS
from django.shortcuts import render_to_response
from django.db.models import Q
from TerraLegal.livro.models import Tbtituloprocesso
import datetime
import urllib2
import json

def lista(request):
    return render_to_response('sicop/relatorio/lista.html',{}, context_instance = RequestContext(request))

#PROCESSOS QUE TEM PECA TECNICA
@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_peca(request):

    if request.method == "POST":
        p_rural = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessorural.objects.filter( tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        p_rural_com_peca = []
        p_rural = consulta.order_by( request.POST['ordenacao'] )
            
        for r in p_rural:
            if Tbpecastecnicas.objects.filter( nrcpfrequerente = r.nrcpfrequerente.replace('.','').replace('-','') ):
                p_rural_com_peca.append( r )
                

        #GERACAO
        nome_relatorio = "relatorio-processos-com-peca"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS COM PECAS TECNICAS"
        planilha_relatorio  = "Processos com peca"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(p_rural_com_peca), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Qtd. Pendencias' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Pendentes' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Notificadas' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("5in")
        sheet.getColumn(4).setWidth("5in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("2in")
        sheet.getColumn(9).setWidth("2in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        
        #DADOS DA CONSULTA
        x = 5
        for obj in p_rural_com_peca:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nmconjuge)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            # buscar todas as pendencias do processo, que nao estao sanadas
            pendencias_pendente = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 2)
              ) 
            pendencias_notificado = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 3)
              ) 
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue( len(pendencias_pendente) + len(pendencias_notificado) )
            # buscando as descricoes das pendencias pendentes
            desc_pendencias = ''
            for pend in pendencias_pendente:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            
            # buscando as descricoes das pendencias  notificadas
            desc_pendencias = ''
            for pend in pendencias_notificado:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/processo_peca.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_processo(request):

    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        pecas_com_proc = []
        pecas = consulta.order_by( request.POST['ordenacao'] )
            
        for p in pecas:
            if len(Tbprocessorural.objects.filter( nrcpfrequerente = p.nrcpfrequerente )) > 0:
                pecas_com_proc.append(p)
  
        #GERACAO
        nome_relatorio = "relatorio-pecas-com-processo"
        titulo_relatorio    = "RELATORIO DAS PECAS TECNICAS COM PROCESSO"
        planilha_relatorio  = "Pecas com processo"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas_com_proc), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas_com_proc:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            if obj.tbmunicipio is None:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue('')    
            else:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbmunicipio.nome_mun)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/peca_processo.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_gleba(request):
    
    #buscar as pecas agrupadas por glebas
    pecas = Tbpecastecnicas.objects.distinct('tbgleba')
    glebas = []
    #buscando as glebas que tem pecas
    for obj in pecas:
        glebas.append( obj.tbgleba )
    #todas as pecas
    #    pecas = Tbpecastecnicas.objects.all()
    for g in glebas:
        qtd = 0
        for p in pecas:
            if p.tbgleba.id == g.id:
                qtd += 1
        print 'Total: '+str(qtd)

    context = dict(         
                        titulo='Relatório das Peças Técnicas por Gleba',
                        total=len(glebas),
                        glebas=glebas
                  )   

    return render_to_response('relatorio/pecas-por-gleba.odt',dictionary=context,format='odt',filename='relatorio-pecas-por-gleba.odt')

#PECAS TECNICAS NAO APROVADAS

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_nao_aprovada(request):
    
    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( Q(stpecatecnica = False, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id) )
        pecas = consulta.order_by( request.POST['ordenacao'] )
          
        #GERACAO
        nome_relatorio = "relatorio-pecas-nao-aprovadas"
        titulo_relatorio    = "RELATORIO DAS PECAS TECNICAS NAO APROVADAS"
        planilha_relatorio  = "Pecas nao aprovadas"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/peca_nao_aprovada.html',{}, context_instance = RequestContext(request))
        
#PECAS TECNICAS REJEITADAS

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_rejeitada(request):

    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( Q(stenviadobrasilia = False, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id) )
        pecas = consulta.order_by( request.POST['ordenacao'] )            
          
        #GERACAO
        nome_relatorio = "relatorio-pecas-rejeitadas"
        titulo_relatorio    = "RELATORIO DAS PECAS TECNICAS REJEITADAS"
        planilha_relatorio  = "Pecas rejeitadas"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/peca_rejeitada.html',{}, context_instance = RequestContext(request))
        
#PECAS TECNICAS SEM PROCESSO

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_sem_processo(request):

    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        pecas_sem_proc = []
        pecas = consulta.order_by( request.POST['ordenacao'] )
            
        for p in pecas:
            if len(Tbprocessorural.objects.filter( nrcpfrequerente = p.nrcpfrequerente )) == 0:
                pecas_sem_proc.append(p)
  
        #GERACAO
        nome_relatorio = "relatorio-pecas-sem-processo"
        titulo_relatorio    = "RELATORIO DAS PECAS TECNICAS SEM PROCESSO"
        planilha_relatorio  = "Pecas sem processo"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas_sem_proc), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas_sem_proc:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            if obj.tbmunicipio is None:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue('')    
            else:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbmunicipio.nome_mun)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/peca_sem_processo.html',{}, context_instance = RequestContext(request))


#PROCESSO SEM PECA CONCLUIR
@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_sem_peca(request):

    if request.method == "POST":
        p_rural = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessorural.objects.filter( tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        p_rural_sem_peca = []
        p_rural = consulta.order_by( request.POST['ordenacao'] )
            
        x = 0
        for rr in p_rural:
            if not Tbpecastecnicas.objects.filter( nrcpfrequerente = rr.nrcpfrequerente ):
                if rr.nrcpfrequerente != '99999999999' and rr.nrcpfrequerente != '00000000000':
                    p_rural_sem_peca.append(rr)

        #GERACAO
        nome_relatorio = "relatorio-processos-sem-peca"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS SEM PECAS TECNICAS"
        planilha_relatorio  = "Processos sem peca"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(p_rural_sem_peca), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Qtd. Pendencias' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Pendentes' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Notificadas' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("5in")
        sheet.getColumn(4).setWidth("5in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("1.5in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in p_rural_sem_peca:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nmconjuge)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            # buscar todas as pendencias do processo, que nao estao sanadas
            pendencias_pendente = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 2)
              ) 
            pendencias_notificado = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 3)
              ) 
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue( len(pendencias_pendente) + len(pendencias_notificado) )
            # buscando as descricoes das pendencias pendentes
            desc_pendencias = ''
            for pend in pendencias_pendente:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            
            # buscando as descricoes das pendencias  notificadas
            desc_pendencias = ''
            for pend in pendencias_notificado:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/processo_sem_peca.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_sem_peca_com_parcela_sigef(request):

    if request.method == "POST":
        p_rural = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessorural.objects.filter( tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        p_rural_sem_peca = []
        p_rural_sem_peca_com_parcela_sigef = []
        p_rural = consulta.order_by( request.POST['ordenacao'] )
            
        x = 0
        for rr in p_rural:
            if not Tbpecastecnicas.objects.filter( nrcpfrequerente = rr.nrcpfrequerente ):
                if rr.nrcpfrequerente != '99999999999' and rr.nrcpfrequerente != '00000000000':
                    p_rural_sem_peca.append(rr)

        for r in p_rural_sem_peca:
            # obj r nao tem peca no sicop
            #buscar no sigef
            try:
                response = urllib2.urlopen('https://sigef.incra.gov.br/api/destinacao/parcelas/?cpf='+r.nrcpfrequerente)
                retorno = json.loads(response.read())
                if retorno['status'] == 'OK':
                    if retorno['parcelas']:
                        p_rural_sem_peca_com_parcela_sigef.append(r)
                        print r.nrcpfrequerente
                x += 1
            except:
                x += 1

            print str( x )+' - '+str(len(p_rural_sem_peca))
                

        #GERACAO
        nome_relatorio = "relatorio-processos-sem-peca-com-parcela-sigef"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS SEM PECAS TECNICAS COM PARCELA(S) NO SIGEF"
        planilha_relatorio  = "Processos sem peca com parcela(s) no SIGEF"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(p_rural_sem_peca_com_parcela_sigef), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Qtd. Pendencias' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Pendentes' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Notificadas' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("5in")
        sheet.getColumn(4).setWidth("5in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("1.5in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in p_rural_sem_peca_com_parcela_sigef:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nmconjuge)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            # buscar todas as pendencias do processo, que nao estao sanadas
            pendencias_pendente = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 2)
              ) 
            pendencias_notificado = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 3)
              ) 
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue( len(pendencias_pendente) + len(pendencias_notificado) )
            # buscando as descricoes das pendencias pendentes
            desc_pendencias = ''
            for pend in pendencias_pendente:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            
            # buscando as descricoes das pendencias  notificadas
            desc_pendencias = ''
            for pend in pendencias_notificado:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/processo_sem_peca_com_parcela_sigef.html',{}, context_instance = RequestContext(request))


@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processos(request):

    if request.method == "POST":
        p_rural = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessorural.objects.filter( tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        p_rural_com_peca = []
        p_rural = consulta.order_by( request.POST['ordenacao'] )
            
        for r in p_rural:
            p_rural_com_peca.append( r )
                

        #GERACAO
        nome_relatorio = "relatorio-todos-processos-rurais"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS RURAIS"
        planilha_relatorio  = "Processos Rurais"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(p_rural_com_peca), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Qtd. Pendencias' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Pendentes' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Notificadas' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("5in")
        sheet.getColumn(4).setWidth("5in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("1.5in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in p_rural_com_peca:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nmconjuge)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            # buscar todas as pendencias do processo, que nao estao sanadas
            pendencias_pendente = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 2)
              ) 
            pendencias_notificado = Tbpendencia.objects.filter( 
               Q(tbprocessobase__id = obj.tbprocessobase.id, tbstatuspendencia__id = 3)
              ) 
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue( len(pendencias_pendente) + len(pendencias_notificado) )
            # buscando as descricoes das pendencias pendentes
            desc_pendencias = ''
            for pend in pendencias_pendente:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            
            # buscando as descricoes das pendencias  notificadas
            desc_pendencias = ''
            for pend in pendencias_notificado:
                desc_pendencias += pend.tbtipopendencia.dspendencia + ' : ' + pend.dsdescricao + ' | '
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue( desc_pendencias )
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/processos.html',{}, context_instance = RequestContext(request))


    #buscar as pecas tecnicas que nao estao ligadas a um processo
    pecas = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    pecas_sem_proc = []
    
    for p in pecas:
        if not Tbprocessorural.objects.filter( nrcpfrequerente = p.nrcpfrequerente ):
            pecas_sem_proc.append(p)
    
    context = dict(        
                    titulo='Relatório das Peças Técnicas sem processo',
                    total=len(pecas_sem_proc),
                    lista=pecas_sem_proc
                )
    
    return render_to_response('relatorio/pecas-sem-processo.odt',dictionary=context,format='odt',filename='relatorio-pecas-sem-processo.odt')

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def varredura_processos(request):
    
    if request.method == "POST":
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessobase.objects.filter( tbclassificacaoprocesso__id = 1, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        processos = consulta.order_by( 'tbcaixa__nmlocalarquivo' )
                            

        #GERACAO
        nome_relatorio = "relatorio-todos-processos"
        titulo_relatorio    = "RELATORIO DE TODOS OS PROCESSOS"
        planilha_relatorio  = "Todos os Processos"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(processos), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Anexos' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("3in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("5in")
        sheet.getColumn(4).setWidth("2.5in")
       
            
        #DADOS DA CONSULTA
        x = 5
        for obj in processos:
            print str(obj.id)
            #verificar se existe obj tipo processo no processobase
            if ( Tbprocessorural.objects.filter( tbprocessobase__id = obj.id ) or Tbprocessoclausula.objects.filter( tbprocessobase__id = obj.id ) or Tbprocessourbano.objects.filter( tbprocessobase__id = obj.id ) ) and obj.nrprocesso != '99999999999999999':
                sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
                #print str(obj.id)
                #buscar nome requerente (rural,clausula) e povoado (urbano)
                requerente = ''
                if obj.tbtipoprocesso.id == 1:
                    requerente = Tbprocessorural.objects.filter( tbprocessobase__id = obj.id )[0].nmrequerente    
                elif obj.tbtipoprocesso.id == 2:
                    requerente = Tbprocessoclausula.objects.filter( tbprocessobase__id = obj.id )[0].nmrequerente    
                else:
                    requerente = Tbprocessourbano.objects.filter( tbprocessobase__id = obj.id )[0].nmpovoado    
                sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(requerente)    

                sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nrprocesso)
                
                #buscar os anexos do obj e concatenar numero com nome requerente ou povoado
                anexo = ''
                anexos = Tbprocessosanexos.objects.filter( tbprocessobase__id = obj.id )
                for an in anexos:
                    if an.tbprocessobase_id_anexo.tbtipoprocesso.id == 1:
                        objan = Tbprocessorural.objects.filter( tbprocessobase__id = an.tbprocessobase_id_anexo.id )
                        anexo += str(objan[0].tbprocessobase.nrprocesso.encode("utf-8"))+':'+objan[0].nmrequerente.encode("utf-8")+"|"
                    elif an.tbprocessobase_id_anexo.tbtipoprocesso.id == 2:
                        objan = Tbprocessoclausula.objects.filter( tbprocessobase__id = an.tbprocessobase_id_anexo.id )
                        anexo += str(objan[0].tbprocessobase.nrprocesso.encode("utf-8"))+':'+str(objan[0].nmrequerente.encode("utf-8"))+"|"
                    else:
                        objan = Tbprocessorural.objects.filter( tbprocessobase__id = an.tbprocessobase_id_anexo.id )
                        anexo += str(objan[0].tbprocessobase.nrprocesso.encode("utf-8"))+':'+str(objan[0].nmpovoado.encode("utf-8"))+"|"
                #print anexo
                sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(anexo.decode("utf-8"))

                sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.tbtipoprocesso.nome.encode("utf-8"))
                x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/processos.html',{}, context_instance = RequestContext(request))


    #buscar as pecas tecnicas que nao estao ligadas a um processo
    pecas = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    pecas_sem_proc = []
    
    for p in pecas:
        if not Tbprocessorural.objects.filter( nrcpfrequerente = p.nrcpfrequerente ):
            pecas_sem_proc.append(p)
    
    context = dict(        
                    titulo='Relatório das Peças Técnicas sem processo',
                    total=len(pecas_sem_proc),
                    lista=pecas_sem_proc
                )
    
    return render_to_response('relatorio/pecas-sem-processo.odt',dictionary=context,format='odt',filename='relatorio-pecas-sem-processo.odt')



#PECAS TECNICAS VALIDADAS

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_validada(request):

    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( Q(stenviadobrasilia = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id) )
        pecas = consulta.order_by( request.POST['ordenacao'] )            
          
        #GERACAO
        nome_relatorio = "relatorio-pecas-validadas"
        titulo_relatorio    = "RELATORIO DAS PECAS TECNICAS VALIDADAS"
        planilha_relatorio  = "Pecas validadas"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/peca_validada.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def pecas(request):

    if request.method == "POST":
        pecas = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        pecas = consulta.order_by( request.POST['ordenacao'] )
              
        #GERACAO
        nome_relatorio = "relatorio-todas-as-pecas-tecnicas"
        titulo_relatorio    = "RELATORIO DE TODAS AS PECAS TECNICAS CADASTRADAS"
        planilha_relatorio  = "Pecas Tecnicas"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(pecas), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Contrato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Entrega' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Area' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Perimetro' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("5in")
        sheet.getColumn(3).setWidth("3.5in")
        sheet.getColumn(4).setWidth("2in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        
        #DADOS DA CONSULTA
        x = 5
        for obj in pecas:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbcontrato.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nrentrega)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nrarea)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrperimetro)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbgleba.nmgleba)    
            if obj.tbmunicipio is None:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue('')    
            else:
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbmunicipio.nome_mun)    
            x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    return render_to_response('sicop/relatorio/pecas.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def etapa_p23(request):
    etapas = Tbetapa.objects.filter( 
        tbtipoprocesso__id = 1, 
        tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by( 'ordem', 'nmfase' )

    if request.method == 'POST':
        etapa = request.POST['etapa']

        p23 = Tbprocessorural.objects.filter(
            tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id,
            tbprocessobase__tbetapaatual__id = etapa    
            )

        for obj in p23 :
            print obj.tbprocessobase.nrprocesso

    return render_to_response('sicop/relatorio/etapa_p23.html',{'etapas':etapas}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def etapa_p80(request):
    etapas = Tbetapa.objects.filter( tbtipoprocesso__id = 2 ).order_by( 'ordem', 'nmfase' )

    if request.method == 'POST':
        etapa = request.POST['etapa']

        consulta = Tbprocessoclausula.objects.filter(
            tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id,
            tbprocessobase__tbetapaatual__id = etapa    
            )

        #GERACAO
        nome_relatorio = "relatorio-processos-etapa"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS DA ETAPA"
        planilha_relatorio  = "Processos na Etapa"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(consulta), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'CPF Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Imovel' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Domicilio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("3in")
        sheet.getColumn(1).setWidth("2.5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("2in")
        sheet.getColumn(4).setWidth("4in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("1.5in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in consulta:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nminteressado)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfinteressado)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.nmimovel)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            if obj.tbprocessobase.tbmunicipiodomicilio is not None:
                sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipiodomicilio.nome_mun)
            else:
                sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue('')
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response


    return render_to_response('sicop/relatorio/etapa_p80.html',{'etapas':etapas}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def etapa_urbano(request):
    etapas = Tbetapa.objects.filter( tbtipoprocesso__id = 3 ).order_by( 'ordem', 'nmfase' )

    if request.method == 'POST':
        etapa = request.POST['etapa']

        urb = Tbprocessourbano.objects.filter(
            tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id,
            tbprocessobase__tbetapaatual__id = etapa    
            )

        for obj in urb :
            print obj.tbprocessobase.nrprocesso

    return render_to_response('sicop/relatorio/etapa_urbano.html',{'etapas':etapas}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def titulos(request):

    caixa = Tbcaixa.objects.filter( blativo = True, tbtipocaixa__nmtipocaixa = 'TIT' ).order_by( 'nmlocalarquivo' )

    if request.method == "POST":
        
        ids = []
        for obj in caixa:
            if request.POST.get(str(obj.id), False):
                ids.append(obj.id)                

        if ids:
            titulos = Tbtituloprocesso.objects.filter( tbtitulo__tbcaixa__tbtipocaixa__nmtipocaixa = 'TIT', tbtitulo__tbcaixa__pk__in = ids ).order_by( 'tbtitulo__cdtitulo' )
        else:
            titulos = Tbtituloprocesso.objects.filter( tbtitulo__tbcaixa__tbtipocaixa__nmtipocaixa = 'TIT' ).order_by( 'tbtitulo__cdtitulo' )

        if titulos:
            #GERACAO
            nome_relatorio = "relatorio-titulos"
            titulo_relatorio    = "RELATORIO DE TITULOS "
            planilha_relatorio  = "Titulos"
            ods = ODS()
            sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(titulos), ods)
            
            # TITULOS DAS COLUNAS
            sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Titulo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Imovel em' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
            sheet.getRow(1).setHeight('20pt')
            sheet.getRow(2).setHeight('20pt')
            sheet.getRow(6).setHeight('20pt')
            
            sheet.getColumn(0).setWidth("2in")
            sheet.getColumn(1).setWidth("1.5in")
            sheet.getColumn(2).setWidth("2in")
            sheet.getColumn(3).setWidth("4.5in")
            sheet.getColumn(4).setWidth("2in")
            sheet.getColumn(5).setWidth("4in")
            sheet.getColumn(6).setWidth("4in")
            sheet.getColumn(7).setWidth("4in")
                
            #DADOS DA CONSULTA
            x = 5
            for obj in titulos:
                sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbtitulo.cdtitulo)
                sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbtitulo.tbtipotitulo.cdtipo)
                sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
                sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
                sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
                sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue( obj.tbtitulo.tbcaixa.nmlocalarquivo )

                r = Tbprocessorural.objects.get( tbprocessobase__id = obj.tbprocessobase.id )
                sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(r.nmrequerente)    
                sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(r.nrcpfrequerente)
                x += 1
                
            #GERACAO DO DOCUMENTO  
            relatorio_ods_base(ods, planilha_relatorio)
            response = HttpResponse(mimetype=ods.mimetype.toString())
            response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
            ods.save(response)
            return response
        
    return render_to_response('sicop/relatorio/titulos.html',{"caixa":caixa}, context_instance = RequestContext(request))


@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def em_programacao_p80(request):

#    if request.method == "POST":
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = []
        checks = Tbchecklistprocessobase.objects.filter( tbprocessobase__tbtipoprocesso__id = 2, tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id, bl_em_programacao = True, tbchecklist__blprogramacao = True ).order_by('tbprocessobase')
        for c in checks:
            consulta.append( Tbprocessoclausula.objects.filter(tbprocessobase__id = c.tbprocessobase.id)[0] )

        #GERACAO
        nome_relatorio = "relatorio-todos-processos-em-programacao"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS EM PROGRAMACAO"
        planilha_relatorio  = "Processos em Programacao"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(consulta), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'CPF Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Imovel' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(10, 6).setAlignHorizontal('center').stringValue( 'Domicilio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(11, 6).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(12, 6).setAlignHorizontal('center').stringValue( 'Programacao' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("3in")
        sheet.getColumn(1).setWidth("2.5in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("2in")
        sheet.getColumn(4).setWidth("4in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("2.5in")
        sheet.getColumn(8).setWidth("2.5in")
        sheet.getColumn(9).setWidth("1.5in")
        sheet.getColumn(10).setWidth("2in")
        sheet.getColumn(11).setWidth("2in")
        sheet.getColumn(12).setWidth("2in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in consulta:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.nminteressado)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfinteressado)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj.nmimovel)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmendereco)
            if obj.tbprocessobase.tbmunicipiodomicilio is not None:
                sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipiodomicilio.nome_mun)
            else:
                sheet.getCell(10, x+2).setAlignHorizontal('center').stringValue('')
            sheet.getCell(11, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nmcontato)
            if obj.tbprocessobase.tbetapaatual is not None:
                sheet.getCell(12, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbetapaatual.titulo)
            else:
                sheet.getCell(12, x+2).setAlignHorizontal('center').stringValue('')
            x += 1
        
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response


@permission_required('sicop.relatorio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def prazos_notificacoes_p80(request):

#    if request.method == "POST":
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        
        prazos = []
        consulta = []
        checksprazos = Tbchecklistprocessobase.objects.filter( tbchecklist__bl_data_prazo = True, blnao_obrigatorio = False, blsanado = False ).order_by('tbprocessobase')
        for obj in checksprazos:
            if obj.dtcustom is not None:
                if obj.tbchecklist.nrprazo is not None:
                    dias = obj.tbchecklist.nrprazo - (datetime.datetime.now() - obj.dtcustom).days
                    if dias >= 0 and dias <= 15:
                        prazos.append( dict({'obj':obj,'dias':dias}) )        
        if prazos:
            for op in prazos:
                proc = Tbprocessoclausula.objects.filter( tbprocessobase__id = op['obj'].tbprocessobase.id )
                consulta.append( dict({'proc':proc[0],'check':op['obj'].tbchecklist.nmchecklist,'etapa':op['obj'].tbchecklist.tbetapa.nmfase,'dias':op['dias']}) )

        #GERACAO
        nome_relatorio = "relatorio-todos-processos-prazo-notificacao"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS COM PRAZOS DE NOTIFICACAO"
        planilha_relatorio  = "Processos com prazos de notificacao"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(consulta), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'CPF Titulado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'CPF Interessado' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(6, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(7, 6).setAlignHorizontal('center').stringValue( 'Etapa' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(8, 6).setAlignHorizontal('center').stringValue( 'Checklist' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(9, 6).setAlignHorizontal('center').stringValue( 'Restante (dias)' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("3in")
        sheet.getColumn(1).setWidth("2in")
        sheet.getColumn(2).setWidth("2.5in")
        sheet.getColumn(3).setWidth("2in")
        sheet.getColumn(4).setWidth("4in")
        sheet.getColumn(5).setWidth("2in")
        sheet.getColumn(6).setWidth("2.5in")
        sheet.getColumn(7).setWidth("3.5in")
        sheet.getColumn(8).setWidth("5in")
        sheet.getColumn(9).setWidth("1.5in")
        
            
        #DADOS DA CONSULTA
        x = 5
        for obj in consulta:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj['proc'].tbprocessobase.tbcaixa.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj['proc'].tbprocessobase.nrprocesso)    
            sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj['proc'].nmrequerente)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj['proc'].nrcpfrequerente)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj['proc'].nminteressado)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj['proc'].nrcpfinteressado)
            sheet.getCell(6, x+2).setAlignHorizontal('center').stringValue(obj['proc'].tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(7, x+2).setAlignHorizontal('center').stringValue(obj['etapa'])
            sheet.getCell(8, x+2).setAlignHorizontal('center').stringValue(obj['check'])
            sheet.getCell(9, x+2).setAlignHorizontal('center').stringValue(obj['dias'])
            x += 1

        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response
