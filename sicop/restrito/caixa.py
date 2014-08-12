from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbcaixa, Tbtipocaixa, AuthUser, Tbprocessobase,\
    Tbpecastecnicas, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano, Tbdivisao
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.forms import FormCaixa
from sicop.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from odslib import ODS
import csv
from reportlab.platypus.tables import Table
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib import styles
from reportlab.lib.units import cm
import webodt
from webodt import converters, ODFDocument
from webodt.converters import converter
from TerraLegal import settings
from django import conf
import os
from django.template.defaultfilters import join
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import File
import django
from django.core.files import storage
from django.db.models import  Q

nome_relatorio      = "relatorio_caixa"
response_consulta  = "/sicop/restrito/caixa/consulta/"
titulo_relatorio    = "Relatorio Caixas"
planilha_relatorio  = "Caixas"

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmlocalarquivo']
        tipo = request.POST['desctipocaixa']
        #lista = Tbcaixa.objects.all().filter( nmlocalarquivo__icontains=nome, tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbcaixa.objects.all().filter( nmlocalarquivo__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id,tbtipocaixa__desctipocaixa__icontains=tipo )
    else:
        #lista = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbcaixa.objects.all().filter(
                Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id)|
                Q(tbtipocaixa__nmtipocaixa__icontains='ENT')
                )
    lista = lista.order_by( 'nmlocalarquivo' )

    
#gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session[nome_relatorio] = lista
    return render_to_response('sicop/restrito/caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.caixa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipocaixa = Tbtipocaixa.objects.all()#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmtipocaixa')
       
    ativo = False
    if request.POST.get('blativo',False):
        ativo = True

    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_caixa = Tbcaixa(
                              nmlocalarquivo = request.POST['nmlocalarquivo'],
                              tbtipocaixa = Tbtipocaixa.objects.get(pk = request.POST['tbtipocaixa']),
                              tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                              blativo = ativo
                              )
            f_caixa.save()
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/restrito/caixa/cadastro.html',{"tipocaixa":tipocaixa}, context_instance = RequestContext(request))

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    tipocaixa = Tbtipocaixa.objects.all()#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmtipocaixa')
    instance = get_object_or_404(Tbcaixa, id=id)
    divisao = Tbdivisao.objects.get(pk = Tbcaixa.objects.get(pk = id).tbdivisao_id)
    
    ativo = False
    if request.POST.get('blativo',False):
        ativo = True
    
    if request.method == "POST":

        if not request.user.has_perm('sicop.caixa_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
       
        form = FormCaixa(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.blativo = ativo
                form.save()
                return HttpResponseRedirect("/sicop/restrito/caixa/edicao/"+str(id)+"/")
    else:
        if divisao.id <> AuthUser.objects.get(pk = request.user.id).tbdivisao.id:
            return HttpResponseRedirect('/excecoes/permissao_negada/')
        form = FormCaixa(instance=instance)
#retornar o conteudo da caixa de acordo com o tipocaixa
#processos = Tbprocessobase.objects.all().filter( tbcaixa__id = id )   

    p_rural = Tbprocessorural.objects.all().filter( tbprocessobase__tbcaixa__id = id, tbprocessobase__tbclassificacaoprocesso__id = 1 )
    p_clausula = Tbprocessoclausula.objects.all().filter( tbprocessobase__tbcaixa__id = id, tbprocessobase__tbclassificacaoprocesso__id = 1 )
    p_urbano = Tbprocessourbano.objects.all().filter( tbprocessobase__tbcaixa__id = id, tbprocessobase__tbclassificacaoprocesso__id = 1 )
    processos = []
    for obj in p_rural:
        processos.append( obj )
    for obj in p_clausula:
        processos.append( obj )
    for obj in p_urbano:
        processos.append( obj )

    
    pecas = Tbpecastecnicas.objects.all().filter( tbcaixa__id = id )    
    conteudo = ""
    if len(processos) > 0:
        request.session['processos-caixa'] = processos
        conteudo = str(len(processos))+" Processo(s)"
    if pecas.count() > 0:
        conteudo += str(pecas.count())+" Peca(s) Tecnica(s)"
        
    if len(processos) <= 0 and pecas.count() <= 0:
        conteudo = "Caixa Vazia"
    
    
    return render_to_response('sicop/restrito/caixa/edicao.html', {"form":form,'processos':processos,'pecas':pecas,'conteudo':conteudo,"tipocaixa":tipocaixa,"divisao":divisao}, context_instance = RequestContext(request))


@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','CAIXA') )
        for obj in lista:
            dados.append( ( obj.nmlocalarquivo , obj.tbtipocaixa.nmtipocaixa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    processos = request.session['processos-caixa']
    
    if processos:
        #GERACAO
        nome_relatorio = "relatorio-processos-caixa"
        titulo_relatorio    = "RELATORIO DOS PROCESSOS DA CAIXA "+processos[0].tbprocessobase.tbcaixa.nmlocalarquivo
        planilha_relatorio  = "Processos da Caixa"
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(processos), ods)
        
        # TITULOS DAS COLUNAS
        sheet.getCell(0, 6).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(1, 6).setAlignHorizontal('center').stringValue( 'Requerente' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(2, 6).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(3, 6).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(4, 6).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getCell(5, 6).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt').setBold(True).setCellColor("#ccff99")
        sheet.getRow(1).setHeight('20pt')
        sheet.getRow(2).setHeight('20pt')
        sheet.getRow(6).setHeight('20pt')
        
        sheet.getColumn(0).setWidth("2in")
        sheet.getColumn(1).setWidth("5in")
        sheet.getColumn(2).setWidth("2in")
        sheet.getColumn(3).setWidth("2.5in")
        sheet.getColumn(4).setWidth("2.5in")
        sheet.getColumn(5).setWidth("2.5in")
            
        #DADOS DA CONSULTA
        x = 5
        for obj in processos:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(3, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(4, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            sheet.getCell(5, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbtipoprocesso.nome)
            if obj.tbprocessobase.tbtipoprocesso.tabela == 'tbprocessourbano':
                sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmpovoado)    
                sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nrcnpj)
            else:
                sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmrequerente)    
                sheet.getCell(2, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
                x += 1
            
        #GERACAO DO DOCUMENTO  
        relatorio_ods_base(ods, planilha_relatorio)
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
        return response

    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([obj.nmlocalarquivo, obj.tbtipocaixa.nmtipocaixa])
        return response
    else:
        return HttpResponseRedirect( response_consulta )


def validacao(request_form):
    warning = True
    if request_form.POST['nmlocalarquivo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a caixa')
        warning = False
    if request_form.POST['tbtipocaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o tipo da caixa')
        warning = False
    return warning