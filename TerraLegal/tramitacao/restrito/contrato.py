from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.tramitacao.forms import FormContrato
from django.contrib import messages
from TerraLegal.tramitacao.models import Tbcontrato, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
from TerraLegal.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
from django.core import serializers
from math import radians, cos, sin, asin, sqrt


nome_relatorio      = "relatorio_contrato"
response_consulta  = "/sicop/contrato/consulta/"
titulo_relatorio    = "Relatorio dos Contratos"
planilha_relatorio  = "Contratos"

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        num = request.POST['nrcontrato']
        nome = request.POST['nmempresa']
        lista = Tbcontrato.objects.all().filter( nrcontrato__icontains=num, nmempresa__contains=nome, tbdivisao__id__in = request.session['divisoes']) #AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbcontrato.objects.all().filter( tbdivisao__id__in = request.session['divisoes'])# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_contrato'] = lista
    return render_to_response('sicop/contrato/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.contrato_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_contrato = Tbcontrato(
                                        nrcontrato = request.POST['nrcontrato'],
                                        nmempresa = request.POST['nmempresa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_contrato.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/contrato/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/contrato/cadastro.html',
                               context_instance = RequestContext(request))

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbcontrato, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.contrato_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_contrato = Tbcontrato(
                                        id = instance.id,
                                        nrcontrato = request.POST['nrcontrato'],
                                        nmempresa = request.POST['nmempresa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_contrato.save()
            return HttpResponseRedirect("/sicop/contrato/edicao/"+str(id)+"/")
    return render_to_response('sicop/contrato/edicao.html', {"contrato":instance}, context_instance = RequestContext(request))


@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NUMERO','EMPRESA') )
        for obj in lista:
            dados.append( ( obj.nrcontrato , obj.nmempresa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Empresa' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nrcontrato)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmempresa)    
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

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Empresa'])
        for obj in lista:
            writer.writerow([obj.nrcontrato, obj.nmempresa])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nrcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do contrato')
        warning = False
    if request_form.POST['nmempresa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da empresa')
        warning = False
    return warning
