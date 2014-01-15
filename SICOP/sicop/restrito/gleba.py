from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormGleba
from sicop.models import Tbgleba, Tbsubarea, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import unicodedata

nome_relatorio      = "relatorio_gleba"
response_consulta  = "/sicop/restrito/gleba/consulta/"
titulo_relatorio    = "Relatorio Glebas"
planilha_relatorio  = "Glebas"


@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmgleba']
        lista = Tbgleba.objects.all().filter( nmgleba__icontains=nome, tbsubarea__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbgleba.objects.all().filter( tbsubarea__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'nmgleba' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_gleba'] = lista
    return render_to_response('sicop/restrito/gleba/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    subarea = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormGleba(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormGleba()
    return render_to_response('sicop/restrito/gleba/cadastro.html',{"form":form,'subarea':subarea}, context_instance = RequestContext(request))

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    subarea = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    instance = get_object_or_404(Tbgleba, id=id)
    if request.method == "POST":
        form = FormGleba(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/gleba/edicao/"+str(id)+"/")
    else:
        form = FormGleba(instance=instance) 
    return render_to_response('sicop/restrito/gleba/edicao.html', {"form":form,'subarea':subarea}, context_instance = RequestContext(request))


@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
    if request_form.POST['nmgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da gleba')
        warning = False
    return warning
