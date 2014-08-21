from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.tramitacao.forms import FormMunicipio
from TerraLegal.tramitacao.models import Tbmunicipio, Tbsubarea, AuthUser, Tbdivisao, Tbuf
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
from TerraLegal.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import os

import xml
import csv
import unicodedata

nome_relatorio      = "relatorio_municipio"
response_consulta  = "/sicop/municipio/consulta/"
titulo_relatorio    = "Relatorio Municipios"
planilha_relatorio  = "Municipios"


@permission_required('sicop.municipio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    # as divisoes somente podem ver suas glebas (classe = 1) Divisoes com classe > 1 podem acessar todas as glebas das classe inferiores
    if request.method == "POST":
        nome = request.POST['nome_mun']
        lista = Tbmunicipio.objects.all().filter( nome_mun__icontains=nome)#, tbuf__id__in=request.session['uf'])# = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id )
    else:
        #lista = Tbgleba.objects.all().filter(tbuf__id=Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id )
        lista = Tbmunicipio.objects.all().filter(codigo_uf__id__in=request.session['uf'])
    lista = lista.order_by( 'nome_mun' )
    
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_municipio'] = lista
    return render_to_response('sicop/municipio/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))


@permission_required('sicop.municipio_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbmunicipio, id=id)
    uf = Tbuf.objects.all()
    
    if request.method == "POST":
        if not request.user.has_perm('sicop.municipio_editar'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = FormMunicipio(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/municipio/edicao/"+str(id)+"/")
    else:
        form = FormMunicipio(instance=instance) 
    return render_to_response('sicop/municipio/edicao.html', {"form":form,'uf':uf}, context_instance = RequestContext(request))


@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','SUBAREA') )
        for obj in lista:
            dados.append( ( obj.nmgleba , obj.tbsubarea.nmsubarea ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'SubArea' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmgleba)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbsubarea.nmsubarea)    
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

@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([ obj.nmgleba.encode('iso-8859-1').strip() , obj.tbsubarea.nmsubarea])
        return response
    else:
        return HttpResponseRedirect( response_consulta )

def validacao(request_form):
    warning = True
    if request_form.POST['nome_mun'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do Municipio')
        warning = False
    return warning
