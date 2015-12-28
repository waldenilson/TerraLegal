from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.models import Tbcaixa, Tbtipocaixa, Tbdivisao, Tbuf
from django.http import HttpResponseRedirect
from django.contrib import messages
from project.tramitacao.forms import FormCaixa, FormDivisao
from project.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from project.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

nome_relatorio      = "relatorio_divisao"
response_consulta  = "/sicop/divisao/consulta/"
titulo_relatorio    = "Relatorio Divisao"
planilha_relatorio  = "Divisoes"


@permission_required('sicop.divisao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmdivisao']
        lista = Tbdivisao.objects.all().filter( nmdivisao__icontains=nome )
    else:
        lista = Tbdivisao.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_divisao'] = lista
    return render_to_response('sicop/divisao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    
@permission_required('sicop.divisao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    uf = Tbuf.objects.all()
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormDivisao(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/divisao/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormDivisao()
    return render_to_response('sicop/divisao/cadastro.html',{"form":form,"uf":uf,"classe":request.session['classe']}, context_instance = RequestContext(request))

@permission_required('sicop.divisao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    uf = Tbuf.objects.all()
    instance = get_object_or_404(Tbdivisao, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.divisao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        form = FormDivisao(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/divisao/edicao/"+str(id)+"/")
    else:
        form = FormDivisao(instance=instance)
    return render_to_response('sicop/divisao/edicao.html', {"form":form,"uf":uf,"classe":request.session['classe']}, context_instance = RequestContext(request))


@permission_required('sicop.divisao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','ESTADO') )
        for obj in lista:
            dados.append( ( obj.nmdivisao , obj.tbuf.nmuf ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.divisao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Estado' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmdivisao)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbuf.nmuf)    
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

@permission_required('sicop.divisao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Estado'])
        for obj in lista:
            writer.writerow([obj.nmdivisao, obj.tbuf.nmuf])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nmdivisao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da dvisao')
        warning = False
    if request_form.POST['tbuf'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o UF')
        warning = False
    return warning