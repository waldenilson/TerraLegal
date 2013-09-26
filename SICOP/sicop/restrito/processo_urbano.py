from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbprocessobase, Tbgleba, Tbmunicipio,\
    Tbcaixa, AuthUser, Tbprocessourbano, Tbsituacaoprocesso, Tbcontrato,\
    Tbsituacaogeo, Tbmovimentacao, Tbclassificacaoprocesso
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
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    contrato = Tbcontrato.objects.all()
    situacaogeo = Tbsituacaogeo.objects.all()
    
    div_processo = "urbano"
    escolha = "tbprocessourbano"  
    
    if request.method == "POST":
        if validacao(request, "cadastro"):
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessourbano' ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 )
                                    )
            f_base.save()
            
            # cadastrando o registro processo urbano
            f_urbano = Tbprocessourbano (
                                       nmpovoado = request.POST['nmpovoado'],
                                       nrcnpj = request.POST['nrcnpj'].replace('.','').replace('/','').replace('-',''),
                                       nrhabitantes = request.POST['nrhabitantes'],
                                       nrdomicilios = request.POST['nrdomicilios'],
                                       nrpregao = request.POST['nrpregao'],
                                       nrarea = request.POST['nrarea'],
                                       nrperimetro = request.POST['nrperimetro'],
                                       tbsituacaogeo = Tbsituacaogeo.objects.get( pk = request.POST['tbsituacaogeo'] ),
                                       tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                       tbprocessobase = f_base,
                                       dtaberturaprocesso = datetime.datetime.strptime( request.POST['dtaberturaprocesso'], "%d/%m/%Y"),
                                       dttitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y"),
                                       )
            f_urbano.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
           
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso,'processo':escolha,'situacaoprocesso':situacaoprocesso, 
         'situacaogeo':situacaogeo,'contrato':contrato,'gleba':gleba,'caixa':caixa,'municipio':municipio,'div_processo':div_processo},
         context_instance = RequestContext(request))     

@login_required
def edicao(request, id):
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    contrato = Tbcontrato.objects.all()
    situacaogeo = Tbsituacaogeo.objects.all()
    
    urbano = get_object_or_404(Tbprocessourbano, id=id)
    base  = get_object_or_404(Tbprocessobase, id=urbano.tbprocessobase.id)

    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" )
    
    # caixa destino
    caixadestino = Tbcaixa.objects.all()
    
    
    if validacao(request, "edicao"):
         # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = base.tbcaixa.id,
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessourbano' ),
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            f_rural = Tbprocessourbano (
                                       id = urbano.id,
                                       nmpovoado = request.POST['nmpovoado'],
                                       nrcnpj = request.POST['nrcnpj'].replace('.','').replace('/','').replace('-',''),
                                       nrhabitantes = request.POST['nrhabitantes'],
                                       nrdomicilios = request.POST['nrdomicilios'],
                                       nrarea = request.POST['nrarea'],
                                       nrperimetro = request.POST['nrperimetro'],
                                       tbsituacaogeo = Tbsituacaogeo.objects.get( pk = request.POST['tbsituacaogeo'] ),
                                       nrpregao = request.POST['nrpregao'],
                                       tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                       tbprocessobase = f_base,
                                       dtaberturaprocesso = datetime.datetime.strptime( request.POST['dtaberturaprocesso'], "%d/%m/%Y"),
                                       dttitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y"),
                                       )
            f_rural.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
           
    
    return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,'contrato':contrato,'situacaogeo':situacaogeo,
                                   'base':base,'movimentacao':movimentacao,
                                   'caixadestino':caixadestino,'urbano':urbano}, context_instance = RequestContext(request))   

def validacao(request_form, metodo):
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
    if request_form.POST['nrarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a Area')
        warning = False
    if request_form.POST['nrperimetro'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Perimetro')
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
    if request_form.POST['tbsituacaogeo'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma situacao GEO')
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
    if request_form.POST['dtaberturaprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a Data da abertura do processo')
        warning = False
    if request_form.POST['dttitulacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a Data da titulacao do processo')
        warning = False
    if metodo == "cadastro":
        if nrProcessoCadastrado( request_form.POST['nrprocesso'].replace('.','').replace('/','').replace('-','') ):
            messages.add_message(request_form,messages.WARNING,'Numero deste processo ja cadastrado')
            warning = False

    return warning 

def nrProcessoCadastrado( numero ):
    result = Tbprocessobase.objects.all().filter( nrprocesso = numero )
    if result:
        return True
    else:
        return False

