from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSubArea
from sicop.models import Tbsubarea, AuthUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_caixa"
response_consulta  = "/sicop/restrito/caixa/consulta/"
titulo_relatorio    = "Relatorio Caixas"
planilha_relatorio  = "Caixas"


@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nmsubarea']
        lista = Tbsubarea.objects.all().filter( nmsubarea__icontains=num, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_sub_area'] = lista
    return render_to_response('sicop/restrito/sub_area/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_subarea = Tbsubarea(
                                        nmsubarea = request.POST['nmsubarea'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_subarea.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/sub_area/cadastro.html',{}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbsubarea, id=id)
    if request.method == "POST":
        if validacao(request):
            f_subarea = Tbsubarea(
                                        id = instance.id,
                                        nmsubarea = request.POST['nmsubarea'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_subarea.save()
            return HttpResponseRedirect("/sicop/restrito/sub_area/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/sub_area/edicao.html', {"subarea":instance}, context_instance = RequestContext(request))


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
    if request_form.POST['nmsubarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a sub area')
        warning = False
    return warning