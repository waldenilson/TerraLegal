from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural, AuthUser
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_consulta,\
    relatorio_csv_base_consulta, relatorio_ods_base_consulta

#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@login_required
def consulta(request):
    lista = []
    if request.method == "POST":
        requerente = request.POST['requerente']
        cpf = request.POST['cpf']
        entrega = request.POST['entrega']
        
        if len(requerente) >= 3:
            lista = Tbpecastecnicas.objects.all().filter( nmrequerente__icontains=requerente, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        else:
            if len(requerente) > 0 and len(requerente) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Requerente.')

        if len(cpf) >= 3:
            lista = Tbpecastecnicas.objects.all().filter( nrcpfrequerente__contains=cpf, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        else:
            if len(cpf) > 0 and len(cpf) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo CPF.')

        if len(entrega) >= 1:
            lista = Tbpecastecnicas.objects.all().filter( nrentrega__contains=entrega, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        else:
            if len(entrega) > 0 and len(entrega) < 1:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Entrega.')

#    else:
#        lista = Tbpecastecnicas.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
#    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_peca_tecnica'] = lista
    return render_to_response('sicop/restrito/peca_tecnica/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Cadastro'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    
    enviadobrasilia = False
    if request.POST.get('stenviadobrasilia',False):
        enviadobrasilia = True
    pecatecnica = False
    if request.POST.get('stpecatecnica',False):
        pecatecnica = True
    anexadoprocesso = False
    if request.POST.get('stanexadoprocesso',False):
        anexadoprocesso = True
    
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
                                   tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao                                   
                                   )
            peca.save()
            return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/") 
    
    return render_to_response('sicop/restrito/peca_tecnica/cadastro.html',{'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))


@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Consulta'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    
    enviadobrasilia = False
    if request.POST.get('stenviadobrasilia',False):
        enviadobrasilia = True
    pecatecnica = False
    if request.POST.get('stpecatecnica',False):
        pecatecnica = True
    anexadoprocesso = False
    if request.POST.get('stanexadoprocesso',False):
        anexadoprocesso = True
    
    peca_obj = get_object_or_404(Tbpecastecnicas, id=id)
        
    if request.method == "POST":       
                 
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
                                   tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                   )
            peca.save()
            return HttpResponseRedirect("/sicop/restrito/peca_tecnica/edicao/"+str(peca_obj.id)+"/")

    processo = Tbprocessorural.objects.all().filter( nrcpfrequerente = peca_obj.nrcpfrequerente.replace('.','').replace('-','') )
    if processo:
        processo = processo[0] 

    return render_to_response('sicop/restrito/peca_tecnica/edicao.html',
                              {'peca':peca_obj,'processo':processo,'caixa':caixa,'contrato':contrato,'gleba':gleba}, 
                            context_instance = RequestContext(request))

def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_peca_tecnica']
    if lista:
        resp = relatorio_pdf_base_consulta(request, lista, 'RELATORIO DAS PECAS TECNICAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/")

def relatorio_ods(request):
    return relatorio_ods_base_consulta(request, 
                                       request.session['relatorio_peca_tecnica'], 
                                       'RELATORIO DAS PECAS TECNICAS',
                                       '/sicop/restrito/peca_tecnica/consulta/')

def relatorio_csv(request):
    return relatorio_csv_base_consulta(request, 
                                       request.session['relatorio_peca_tecnica'], 
                                       'RELATORIO DAS PECAS TECNICAS',
                                       '/sicop/restrito/peca_tecnica/consulta/')

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
