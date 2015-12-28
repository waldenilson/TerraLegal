from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from project.tramitacao.models import Tbsituacao
from django.contrib import messages
from project.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from project.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS

nome_relatorio      = "relatorio_tipo_situacao"
response_consulta  = "/sicop/tipo_caixa/consulta/"
titulo_relatorio    = "Relatorio dos Tipos de Caixa"
planilha_relatorio  = "Tipos de Caixa"
'''
definir o que faz esse modulo
'''

@permission_required('sicop.tipo_situacao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['cdTabela']
        lista = Tbsituacao.objects.all().filter(cdTabela__icontains=nome)
    else:
        lista = Tbsituacao.objects.all()
    lista = lista.order_by( 'cdTabela' )
    
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_situacao'] = lista
    return render_to_response('sicop/situacao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    
@permission_required('sicop.tipo_situacao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')    
        if validacao(request):
            f_situacao = Tbsituacao(cdTabela = request.POST['cdTabela'],
                                    dsSituacao = request.POST['dsSituacao'],)
            f_situacao.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/situacao/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/situacao/cadastro.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_situacao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbsituacao, id=id)
    if request.method == "POST":

        if not request.user.has_perm('sicop.tipo_situacao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        if validacao(request):
            f_situacao = Tbsituacao(
                                        id = instance.id,
                                        cdTabela = request.POST['cdTabela'],
                                        dsSituacao = request.POST['dsSituacao'],
                                        
                                      )
            f_situacao.save()
            return HttpResponseRedirect("/sicop/situacao/edicao/"+str(id)+"/")
    return render_to_response('sicop/situacao/edicao.html', {"situacao":instance}, context_instance = RequestContext(request))


@permission_required('sicop.tipo_situacao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.tipo_situacao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.tipo_situacao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
    if request_form.POST['cdTabela'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe uma tabela para o tipo')
        warning = False
    if request_form.POST['dsSituacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a descricao da situacao da tabela')
        warning = False
        
        
    return warning
