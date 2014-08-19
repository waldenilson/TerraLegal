# -*- coding: UTF-8 -*-
from django.template.context import RequestContext
from sicop.models import Tbpecastecnicas, \
    Tbprocessorural, AuthUser, Tbmunicipio, Tbprocessoclausula, Tbpendencia
from sicop.relatorio_base import relatorio_ods_base_header,\
    relatorio_ods_base
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponse
from odslib import ODS
from django.shortcuts import render_to_response
from django.db.models import Q

def lista(request):
    return render_to_response('sicop/restrito/relatorio/lista.html',{}, context_instance = RequestContext(request))

#PROCESSOS QUE TEM PECA TECNICA
@permission_required('sicop.relatorio_processo_peca_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/processo_peca.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_peca_sem_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/peca_processo.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_peca_gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
        print 'Gleba: '+str(g.nmgleba)
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

@permission_required('sicop.relatorio_peca_nao_aprovada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/peca_nao_aprovada.html',{}, context_instance = RequestContext(request))
        
#PECAS TECNICAS REJEITADAS

@permission_required('sicop.relatorio_peca_rejeitada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/peca_rejeitada.html',{}, context_instance = RequestContext(request))
        
#PECAS TECNICAS SEM PROCESSO

@permission_required('sicop.relatorio_peca_sem_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/peca_sem_processo.html',{}, context_instance = RequestContext(request))


#PROCESSO SEM PECA CONCLUIR

@permission_required('sicop.relatorio_processo_peca_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_sem_peca(request):

    if request.method == "POST":
        p_rural = []
        #CONSULTA ORDENADA E/OU BASEADA EM FILTROS DE PESQUISA
        consulta = Tbprocessorural.objects.filter( tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        p_rural_com_peca = []
        p_rural = consulta.order_by( request.POST['ordenacao'] )
            
        for r in p_rural:
            if not Tbpecastecnicas.objects.filter( nrcpfrequerente = r.nrcpfrequerente ):
                p_rural_com_peca.append( r )
                

        #GERACAO
        nome_relatorio = "relatorio-processos-sem-peca"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS SEM PECAS TECNICAS"
        planilha_relatorio  = "Processos sem peca"
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

    return render_to_response('sicop/restrito/relatorio/processo_sem_peca.html',{}, context_instance = RequestContext(request))


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


@permission_required('sicop.relatorio_processo_peca_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/processos.html',{}, context_instance = RequestContext(request))


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

@permission_required('sicop.relatorio_peca_validada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/peca_validada.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.relatorio_peca_sem_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

    return render_to_response('sicop/restrito/relatorio/pecas.html',{}, context_instance = RequestContext(request))
