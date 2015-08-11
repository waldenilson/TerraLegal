from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from TerraLegal.tramitacao.models import Tbcaixa, Tbtipocaixa, AuthUser, Tbprocessobase,\
    Tbpecastecnicas, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano, Tbdivisao,\
    Tbetapa, Tbtipoprocesso, Tbchecklist
from django.http import HttpResponseRedirect
from django.contrib import messages
from TerraLegal.tramitacao.forms import FormCaixa
from TerraLegal.tramitacao.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from odslib import ODS
import csv
from reportlab.platypus.tables import Table
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib import styles
from reportlab.lib.units import cm
from TerraLegal import settings
from django import conf
import os
from django.template.defaultfilters import join
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import File
import django
from django.core.files import storage
from django.db.models import  Q

nome_relatorio      = "relatorio_checklist"
response_consulta  = "/sicop/checklist/consulta/"
titulo_relatorio    = "Relatorio Checklist"
planilha_relatorio  = "Checklist"

@permission_required('sicop.checklist_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmchecklist']
        pesquisa_etapa = request.POST['pesquisa_etapa']
        #lista = Tbcaixa.objects.all().filter( nmlocalarquivo__icontains=nome, tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbchecklist.objects.filter( nmchecklist__icontains=nome, tbetapa__nmfase__icontains=pesquisa_etapa, tbetapa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        #lista = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbchecklist.objects.filter( tbetapa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        
    lista = lista.order_by( 'nmchecklist' )
    
#gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session[nome_relatorio] = lista
    return render_to_response('sicop/checklist/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.checklist_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    fase = Tbetapa.objects.filter(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id).order_by('id')
    
    if request.method == "POST":
        next = request.GET.get('next', '/')

        f_checklist = Tbchecklist(
                              nmchecklist = request.POST['nmchecklist'],
                              dschecklist = request.POST['dschecklist'],
                              blcustomdate = request.POST.get('blcustomdate',False),
                              bl_data_prazo = request.POST.get('bl_data_prazo',False),
                              blcustomtext = request.POST.get('blcustomtext',False),
                              blprogramacao = request.POST.get('blprogramacao',False),
                              lbcustomdate = request.POST['lbcustomdate'],
                              lbcustomtext = request.POST['lbcustomtext']
                              )
        
        if request.POST['nrprazo'] == '':
            f_checklist.nrprazo = 0
        else:
            f_checklist = request.POST['nrprazo']

        if request.POST['tbfase'] != '':
            request.session['etapachecklist'] = request.POST['tbfase']

        try:
            f_checklist.tbetapa = Tbetapa.objects.get(pk = request.session['etapachecklist'])
        except:
            f_checklist.tbetapa = Tbetapa.objects.get(pk = request.POST['tbfase'])
                              
        f_checklist.save()

        if next == "/":
            return HttpResponseRedirect('sicop/checklist/cadastro')
        else:    
            return HttpResponseRedirect(next)
    return render_to_response('sicop/checklist/cadastro.html',{"fase":fase}, context_instance = RequestContext(request))


@permission_required('sicop.checklist_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbchecklist, id=id)
    fase = Tbetapa.objects.filter(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id).order_by('id')
          
    if request.method == "POST":
        
        if not request.user.has_perm('sicop.checklist_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        next = request.GET.get('next', '/')
        if validacao(request):
            f_checklist = Tbchecklist(
                              id = instance.id,
                              nmchecklist = request.POST['nmchecklist'],
                              tbetapa = Tbetapa.objects.get(pk = request.POST['tbfase']),
                              dschecklist = request.POST['dschecklist'],
                              blcustomdate = request.POST.get('blcustomdate',False),
                              bl_data_prazo = request.POST.get('bl_data_prazo',False),
                              blcustomtext = request.POST.get('blcustomtext',False),
                              blprogramacao = request.POST.get('blprogramacao',False),                              
                              lbcustomdate = request.POST['lbcustomdate'],
                              lbcustomtext = request.POST['lbcustomtext']
                              )

            if request.POST['nrprazo'] == '':
                f_checklist.nrprazo = 0
            else:
                f_checklist.nrprazo = request.POST['nrprazo']
            f_checklist.save()

            if next == "/":
                return HttpResponseRedirect("/sicop/checklist/edicao/"+str(id)+"/")
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/checklist/edicao.html',{"checklist":instance,"fase":fase}, context_instance = RequestContext(request))

@permission_required('sicop.checklist_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.checklist_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbtipocaixa.nmtipocaixa)    
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.checklist_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
    nome = request_form.POST['nmchecklist']
#    pos = request_form.POST['ordem']
    fase = request_form.POST['tbfase']
    
    if fase == '':
        messages.add_message(request_form,messages.WARNING,'Informe uma etapa para o checklist')
        warning = False
    elif nome == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para o checklist.')
        warning = False
#    else:
#        list = []
        # ordem com tipoprocesso eh unico
#        list = Tbfase.objects.filter( ordem= int(pos), tbtipoprocesso__id = tipoprocesso  )
#        if list:
#            messages.add_message(request_form,messages.WARNING,'Numero da ordem usado por outra fase desse tipo de processo')
#            warning = False
#        list = []
        # nome com tipoprocesso eh unico
#        list = Tbfase.objects.filter( nmfase__icontains = nome, tbtipoprocesso__id = tipoprocesso  )
#        if list:
#            messages.add_message(request_form,messages.WARNING,'Informe outro nome da fase')
#            warning = False
    
    return warning