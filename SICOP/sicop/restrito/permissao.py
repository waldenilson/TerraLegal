from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbcaixa, Tbtipocaixa, AuthUser, Tbprocessobase,\
    Tbpecastecnicas, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano, Tbdivisao,\
    AuthPermission, DjangoContentType
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

nome_relatorio      = "relatorio_permissao"
response_consulta  = "/sicop/restrito/permissao/consulta/"
titulo_relatorio    = "Relatorio Permissoes"
planilha_relatorio  = "Permissoes"

@permission_required('sicop.permissao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    lista = AuthPermission.objects.all()
    if request.method == "POST":
        nome = request.POST['nome']
        lista = AuthPermission.objects.filter( name__icontains=nome )
        lista = lista.order_by( 'name' )
    
#gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session[nome_relatorio] = lista
    return render_to_response('sicop/restrito/permissao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.permissao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    content = DjangoContentType.objects.all()#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmtipocaixa')
       
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_permissao = AuthPermission(
                              name = request.POST['nome'],
                              codename = request.POST['codenome'],
                              content_type = DjangoContentType.objects.get(pk = request.POST['content'])
                              )
            f_permissao.save()
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/restrito/permissao/cadastro.html',{"content":content}, context_instance = RequestContext(request))

@permission_required('sicop.permissao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    content = DjangoContentType.objects.all()#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmtipocaixa')
    instance = get_object_or_404(AuthPermission, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.permissao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_permissao = AuthPermission(
                              id = instance.id,
                              name = request.POST['nome'],
                              codename = request.POST['codenome'],
                              content_type = DjangoContentType.objects.get(pk = request.POST['content'])
                              )
            f_permissao.save()
 
        return HttpResponseRedirect("/sicop/restrito/permissao/edicao/"+str(id)+"/")
    
    return render_to_response('sicop/restrito/permissao/edicao.html', {"permissao":instance,"content":content}, context_instance = RequestContext(request))


@permission_required('sicop.permissao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.permissao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.permissao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a permissao')
        warning = False
    if request_form.POST['codenome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um codenome para a permissao')
        warning = False
    return warning