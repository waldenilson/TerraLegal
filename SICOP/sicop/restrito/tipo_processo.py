from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoProcesso
from sicop.models import Tbtipoprocesso, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_tipo_processo"
response_consulta  = "/sicop/restrito/tipo_processo/consulta/"
titulo_relatorio    = "Relatorio dos Tipos de Processos"
planilha_relatorio  = "Tipos de Processos"


@permission_required('sicop.tipo_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nome']
        lista = Tbtipoprocesso.objects.all().filter( nome__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_processo'] = lista
    return render_to_response('sicop/restrito/tipo_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_processo_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_tipoprocesso = Tbtipoprocesso(
                                                nome = request.POST['nome'],
                                                tabela = request.POST['tabela'],
                                                coridentificacao = request.POST['coridentificacao'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_tipoprocesso.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_processo/consulta/") 
    return render_to_response('sicop/restrito/tipo_processo/cadastro.html', context_instance = RequestContext(request))

@permission_required('sicop.tipo_processo_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbtipoprocesso, id=id)
    if request.method == "POST":
        if validacao(request):
            f_tipoprocesso = Tbtipoprocesso(
                                                id = instance.id,
                                                nome = request.POST['nome'],
                                                tabela = request.POST['tabela'],
                                                coridentificacao = request.POST['coridentificacao'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_tipoprocesso.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_processo/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/tipo_processo/edicao.html', {"tipoprocesso":instance}, context_instance = RequestContext(request))


@permission_required('sicop.tipo_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','') )
        for obj in lista:
            dados.append( ( obj.nome, '' ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.tipo_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nome)
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

@permission_required('sicop.tipo_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome'])
        for obj in lista:
            writer.writerow([obj.nome])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo processo')
        warning = False
    if request_form.POST['tabela'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a tabela do tipo processo')
        warning = False
    return warning
