# coding: utf-8
from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from TerraLegal.tramitacao.forms import FormPecasTecnicas
from TerraLegal.tramitacao.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural, AuthUser, Tbdivisao, Tbmunicipio
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from TerraLegal.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS
from django.db.models import  Q



nome_relatorio      = "relatorio_peca_tecnica"
response_consulta  = "/sicop/peca_tecnica/consulta/"
titulo_relatorio    = "Relatorio Pecas Tecnicas"
planilha_relatorio  = "Pecas Tecnicas"


#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    lista = []
    if request.method == "POST":
        requerente = request.POST['requerente']
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        entrega = request.POST['entrega']
        
        if len(requerente) >= 3:
            #lista = Tbpecastecnicas.objects.all().filter( nmrequerente__icontains=requerente, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmrequerente')
            lista = Tbpecastecnicas.objects.all().filter( nmrequerente__icontains=requerente, tbdivisao__id__in = request.session['divisoes']).order_by('nmrequerente')
        else:
            if len(requerente) > 0 and len(requerente) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Requerente.')

        if len(cpf) >= 3:
            #lista = Tbpecastecnicas.objects.all().filter( nrcpfrequerente__contains=cpf, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmrequerente')
            lista = Tbpecastecnicas.objects.all().filter( nrcpfrequerente__contains=cpf, tbdivisao__id__in=request.session['divisoes']).order_by('nmrequerente')
        else:
            if len(cpf) > 0 and len(cpf) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo CPF.')

        if len(entrega) >= 1:
            #lista = Tbpecastecnicas.objects.all().filter( nrentrega__contains=entrega, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmrequerente')
            lista = Tbpecastecnicas.objects.all().filter( nrentrega__contains=entrega, tbdivisao__id__in=request.session['divisoes']).order_by('nmrequerente')
        else:
            if len(entrega) > 0 and len(entrega) < 1:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Entrega.')

#    else:
#        lista = Tbpecastecnicas.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
#    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_peca_tecnica'] = lista
    return render_to_response('sicop/peca_tecnica/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.peca_tecnica_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    #alterado abaixo para retornar os contratos, glebas e caixas de acordo com a hierarquia dass divisoes.
    #contrato = Tbcontrato.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nrcontrato')
    #caixa = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo')
    #gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    contrato = Tbcontrato.objects.all().filter( tbdivisao__id__in = request.session['divisoes']).order_by('nrcontrato')
    gleba = Tbgleba.objects.all().filter( tbuf__id__in= request.session['uf']).order_by('nmgleba')
    caixa = Tbcaixa.objects.all().filter(
                Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id)|
                Q(tbtipocaixa__nmtipocaixa__icontains='ENT')
                ).order_by('nmlocalarquivo')
    
    enviadobrasilia = False
    if request.POST.get('stenviadobrasilia',False):
        enviadobrasilia = True
    pecatecnica = False
    if request.POST.get('stpecatecnica',False):
        pecatecnica = True
    anexadoprocesso = False
    if request.POST.get('stanexadoprocesso',False):
        anexadoprocesso = True
    assentamento = False
    if request.POST.get('stassentamento',False):
        assentamento = True
        
    if request.method == "POST":
        if validacao(request):            

            area = request.POST['nrarea'].replace(',','.')
            if not area:
                area = None
                        
            perimetro = request.POST['nrperimetro'].replace(',','.')
            if not perimetro:
                perimetro = None

            
            peca = Tbpecastecnicas(
                                   tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                   tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                   tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                   nrarea = area,
                                   nrperimetro = perimetro,
                                   dsobservacao = request.POST['dsobservacao'],
                                   nrentrega = request.POST['nrentrega'],
                                   nmrequerente = request.POST['nmrequerente'],
                                   nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                   stanexadoprocesso = anexadoprocesso,
                                   stpecatecnica = pecatecnica,
                                   stenviadobrasilia = enviadobrasilia,
                                   tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                                   tbmunicipio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipio']),
                                   stassentamento = assentamento                               
                                   )
            peca.save()
            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            return HttpResponseRedirect("/sicop/peca_tecnica/consulta/") 
    
    return render_to_response('sicop/peca_tecnica/cadastro.html',{'caixa':caixa,'contrato':contrato,'gleba':gleba,'municipio':municipio}, context_instance = RequestContext(request))


@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    #contrato = Tbcontrato.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nrcontrato')
    #caixa = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo')
    #gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    caixa = Tbcaixa.objects.all().filter( tbdivisao__id__in = request.session['divisoes']).order_by('nmlocalarquivo')#AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo')
    contrato = Tbcontrato.objects.all().filter( tbdivisao__id__in = request.session['divisoes']).order_by('nrcontrato') #= AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nrcontrato')
    gleba = Tbgleba.objects.all().filter( tbuf__id__in=request.session['uf']).order_by('nmgleba')#  Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
     
    enviadobrasilia = False
    if request.POST.get('stenviadobrasilia',False):
        enviadobrasilia = True
    pecatecnica = False
    if request.POST.get('stpecatecnica',False):
        pecatecnica = True
    anexadoprocesso = False
    if request.POST.get('stanexadoprocesso',False):
        anexadoprocesso = True
    assentamento = False
    if request.POST.get('stassentamento',False):
        assentamento = True
        
    
    peca_obj = get_object_or_404(Tbpecastecnicas, id=id)
        
    if request.method == "POST":       

        if not request.user.has_perm('sicop.peca_tecnica_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
                 
        if validacao(request):
 
            area = request.POST['nrarea'].replace(',','.')
            if not area:
                area = None
                        
            perimetro = request.POST['nrperimetro'].replace(',','.')
            if not perimetro:
                perimetro = None

            
            peca = Tbpecastecnicas(
                                   id = peca_obj.id,
                                   tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                   tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                   tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                   nrarea = area,
                                   nrperimetro = perimetro,
                                   dsobservacao = request.POST['dsobservacao'],
                                   nrentrega = request.POST['nrentrega'],
                                   nmrequerente = request.POST['nmrequerente'],
                                   nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                   stanexadoprocesso = anexadoprocesso,
                                   stpecatecnica = pecatecnica,
                                   stenviadobrasilia = enviadobrasilia,
                                   tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                                   tbmunicipio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipio']),
                                   stassentamento = assentamento
    
                                   )
            peca.save()
            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            return HttpResponseRedirect("/sicop/peca_tecnica/edicao/"+str(peca_obj.id)+"/")

    processo = Tbprocessorural.objects.all().filter( nrcpfrequerente = peca_obj.nrcpfrequerente.replace('.','').replace('-','') )
    if processo:
        processo = processo[0] 

    return render_to_response('sicop/peca_tecnica/edicao.html',
                              {'peca':peca_obj,'processo':processo,'caixa':caixa,'contrato':contrato,'gleba':gleba,'municipio':municipio}, 
                            context_instance = RequestContext(request))


@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('CPF','CAIXA') )
        for obj in lista:
            dados.append( ( obj.nrcpfrequerente , obj.tbcaixa.nmlocalarquivo ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Caixa' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nrcpfrequerente)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbcaixa.nmlocalarquivo)    
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

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['CPF', 'Caixa'])
        for obj in lista:
            writer.writerow([obj.nrcpfrequerente, obj.tbcaixa.nmlocalarquivo])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['tbcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione o Contrato')
        warning = False
    if request_form.POST['nrentrega'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da entrega')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um CPF valido para o requerente')
        warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do requerente maior que 4 letras')
        warning = False
    if request_form.POST['tbcaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione uma Caixa') 
        warning = False
#    if request_form.POST['nrarea'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe o numero da area')
#        warning = False
#    if request_form.POST['nrperimetro'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe o numero do perimetro')
#        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione uma Gleba') 
        warning = False
    return warning
