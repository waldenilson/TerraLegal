from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormStatusPendencia
from sicop.models import Tbstatuspendencia, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['dspendencia']
        lista = Tbstatuspendencia.objects.all().filter( dspendencia__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbstatuspendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_status_pendencia'] = lista
    return render_to_response('sicop/restrito/status_pendencia/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_statuspendencia = Tbstatuspendencia(
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_statuspendencia.save()
            return HttpResponseRedirect("/sicop/restrito/status_pendencia/consulta/") 
    return render_to_response('sicop/restrito/status_pendencia/cadastro.html',{}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbstatuspendencia, id=id)
    if request.method == "POST":
        if validacao(request):
            f_statuspendencia = Tbstatuspendencia(
                                        id = instance.id,
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_statuspendencia.save()
            return HttpResponseRedirect("/sicop/restrito/status_pendencia/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/status_pendencia/edicao.html', {"statuspendencia":instance}, context_instance = RequestContext(request))

def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_caixa']
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, 'relatorio-caixas')   
        elements=[]
        
        dados = relatorio_pdf_base_header_title('Relatorio Caixas')
        dados.append( ('NOME','CAIXA') )
        for obj in lista:
            dados.append( ( obj.nmlocalarquivo , obj.tbtipocaixa.nmtipocaixa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect("/sicop/restrito/caixa/consulta/")

def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_caixa']
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header('Caixas','Relatorio Caixas', ods)
        
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
       
        relatorio_ods_base(ods, 'caixas')
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename="relatorio-caixas.ods"'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( "/sicop/restrito/caixa/consulta" )

def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_caixa']
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, 'relatorio-caixas')
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([obj.nmlocalarquivo, obj.tbtipocaixa.nmtipocaixa])
        return response
    else:
        return HttpResponseRedirect( '/sicop/restrito/caixa/consulta/' )


def validacao(request_form):
    warning = True
    if request_form.POST['dspendencia'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do status pendencia')
        warning = False
    return warning
