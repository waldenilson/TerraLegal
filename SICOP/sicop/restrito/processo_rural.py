from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/rural/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    
    div_processo = "rural"
    escolha = "tbprocessorural"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):
            
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            tem_conjuge = False
            if request.POST['nmconjuge'] != '' and request.POST['nrcpfconjuge'] != '':
                tem_conjuge = True
            f_rural = Tbprocessorural (
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmconjuge = request.POST['nmconjuge'],
                                       nrcpfconjuge = request.POST['nrcpfconjuge'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       blconjuge = tem_conjuge,
                                       tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 )
                                       )
            f_rural.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'gleba':gleba,'situacaoprocesso':situacaoprocesso,'caixa':caixa,'municipio':municipio,'tipoprocesso':tipoprocesso, 'processo':escolha, 'div_processo':div_processo}, context_instance = RequestContext(request))    
  
@login_required
def edicao(request, id):
    
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    
    rural = get_object_or_404(Tbprocessorural, id=id)
    base  = get_object_or_404(Tbprocessobase, id=rural.tbprocessobase.id)
    
    if validacao(request, "edicao"):
         # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            tem_conjuge = False
            if request.POST['nmconjuge'] != '' and request.POST['nrcpfconjuge'] != '':
                tem_conjuge = True
            f_rural = Tbprocessorural (
                                       id = rural.id,
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmconjuge = request.POST['nmconjuge'],
                                       nrcpfconjuge = request.POST['nrcpfconjuge'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       blconjuge = tem_conjuge,
                                       tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 )
                                       )
            f_rural.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
    
    return render_to_response('sicop/restrito/processo/rural/edicao.html',
                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,
                                   'base':base,'rural':rural},
                               context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if request_form.POST['nrprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
        warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do requerente')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CPF do requerente')
        warning = False
    if request_form.POST['tbcaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
        warning = False
    if request_form.POST['tbsituacaoprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha a situacao do processo')
        warning = False
    
    # validacao dos dados de conjuge
    if request_form.POST['nmconjuge'] != '' and request_form.POST['nrcpfconjuge'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe os dados do conjuge corretamente')
        warning = False
    else:
        if request_form.POST['nmconjuge'] == '' and request_form.POST['nrcpfconjuge'] != '':
            messages.add_message(request_form,messages.WARNING,'Informe os dados do conjuge corretamente')
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
