from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoCaixa
from django.http import HttpResponseRedirect
from sicop.models import Tbtipocaixa, AuthUser
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_tipo_caixa"
response_consulta  = "/sicop/tipo_caixa/consulta/"
titulo_relatorio    = "Relatorio dos Tipos de Caixa"
planilha_relatorio  = "Tipos de Caixa"


@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmtipocaixa']
        lista = Tbtipocaixa.objects.all().filter( nmtipocaixa__icontains=nome)#, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipocaixa.objects.all()#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'nmtipocaixa' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_caixa'] = lista
    return render_to_response('sicop/tipo_caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@permission_required('sicop.tipo_caixa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')    
        if validacao(request):
            f_tipocaixa = Tbtipocaixa(
                                        nmtipocaixa = request.POST['nmtipocaixa'],
                                        desctipocaixa = request.POST['desctipocaixa'],
                                        #tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipocaixa.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/tipo_caixa/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/tipo_caixa/cadastro.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbtipocaixa, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.tipo_caixa_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_tipocaixa = Tbtipocaixa(
                                        id = instance.id,
                                        nmtipocaixa = request.POST['nmtipocaixa'],
                                        desctipocaixa = request.POST['desctipocaixa'],
                                        #tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipocaixa.save()
            return HttpResponseRedirect("/sicop/tipo_caixa/edicao/"+str(id)+"/")
    return render_to_response('sicop/tipo_caixa/edicao.html', {"tipocaixa":instance}, context_instance = RequestContext(request))


@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','DESCRICAO') )
        for obj in lista:
            dados.append( ( obj.nmtipocaixa , obj.desctipocaixa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Descricao' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmtipocaixa)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.desctipocaixa)    
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

@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Descricao'])
        for obj in lista:
            writer.writerow([obj.nmtipocaixa, obj.desctipocaixa])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nmtipocaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para o tipo caixa')
        warning = False
    return warning
