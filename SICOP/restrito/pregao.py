from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormContrato
from django.contrib import messages
from sicop.models import Tbcontrato, AuthUser, Tbpregao
from django.http.response import HttpResponseRedirect, HttpResponse
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_pregao"
response_consulta  = "/sicop/restrito/pregao/consulta/"
titulo_relatorio    = "Relatorio Pregoes"
planilha_relatorio  = "Pregoes"


@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        num = request.POST['nrpregao']
        descricao = request.POST['dspregao']
        lista = Tbpregao.objects.all().filter( nrpregao__icontains=num, dspregao__icontains=descricao, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbpregao.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_pregao'] = lista
    return render_to_response('sicop/restrito/pregao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.pregao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_pregao = Tbpregao(
                                        nrpregao = request.POST['nrpregao'],
                                        dspregao = request.POST['dspregao'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_pregao.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/pregao/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/pregao/cadastro.html',
                               context_instance = RequestContext(request))

@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbpregao, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.pregao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_pregao = Tbpregao(
                                        id = instance.id,
                                        nrpregao = request.POST['nrpregao'],
                                        dspregao = request.POST['dspregao'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_pregao.save()
            return HttpResponseRedirect("/sicop/restrito/pregao/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/pregao/edicao.html', {"pregao":instance}, context_instance = RequestContext(request))


@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NUMERO','DESCRICAO') )
        for obj in lista:
            dados.append( ( obj.nrpregao , obj.dspregao ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Numero' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Descricao' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nrpregao)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.dspregao)    
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

@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Numero', 'Descricao'])
        for obj in lista:
            writer.writerow([obj.nrpregao, obj.dspregao])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nrpregao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do pregao')
        warning = False
    return warning
