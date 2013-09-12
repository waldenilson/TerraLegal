from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbprocessobase, Tbgleba, Tbmunicipio,\
    Tbcaixa, AuthUser, Tbprocessourbano, Tbsituacaoprocesso, Tbcontrato
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.forms import FormProcessoUrbano
import datetime

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/urbano/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    municipio = Tbmunicipio.objects.all()
    contrato = Tbcontrato.objects.all()
    
    div_processo = "urbano"
    escolha = "tbprocessourbano"  
    
    if request.method == "POST":
        if validacao(request):
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( pk = 3 ),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            f_rural = Tbprocessourbano (
                                       nmpovoado = request.POST['nmpovoado'],
                                       nrcnpj = request.POST['nrcnpj'].replace('.','').replace('/','').replace('-',''),
                                       nrhabitantes = request.POST['nrhabitantes'],
                                       nrdomicilios = request.POST['nrdomicilios'],
                                       nrpregao = request.POST['nrpregao'],
                                       tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                       tbprocessobase = f_base,
                                       dtaberturaprocesso = datetime.datetime.now()
                                       )
            f_rural.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
           
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso,'processo':escolha,'situacaoprocesso':situacaoprocesso, 'contrato':contrato,'gleba':gleba,'caixa':caixa,'municipio':municipio,'div_processo':div_processo},
         context_instance = RequestContext(request))     

@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/urbano/edicao.html',{}, context_instance = RequestContext(request))    

def validacao(request_form):
    warning = True
    if request_form.POST['nrprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
        warning = False
    if request_form.POST['nrcnpj'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CNPJ')
        warning = False
    if request_form.POST['nmpovoado'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do povoado')
        warning = False
    if request_form.POST['tbcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha o Contrato')
        warning = False
    if request_form.POST['nrhabitantes'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Numero de habitantes')
        warning = False
    if request_form.POST['nrdomicilios'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Numero de Domicilios')
        warning = False
    if request_form.POST['nrpregao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Numero do Pregao')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
        warning = False
    if request_form.POST['tbcaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
        warning = False
    return warning 
