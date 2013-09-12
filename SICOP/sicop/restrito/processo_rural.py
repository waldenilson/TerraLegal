from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso,\
    Tbconjuge, Tbsituacaoprocesso
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
    municipio = Tbmunicipio.objects.all()
    
    div_processo = "rural"
    escolha = "tbprocessorural"
    
    if request.method == "POST":
        if validacao(request):
            
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( pk = 1 ),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            f_rural = Tbprocessorural (
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       dtcadastrosistema = datetime.datetime.now(),
                                       tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 )
                                       )
            f_rural.save()
            
            # cadastrando o conjuge do processo ( caso seja informado )
            # se nome conjuge digitado e cpf digitado: validacao ok
            # se cpf nao digitado: desconsiderar conjuge
            if request.POST['nrcpfconjuge'] != '' and request.POST['nmconjuge'] != '':
                f_conjuge = Tbconjuge (
                                       tbprocessobase = f_base,
                                       nrcpf = request.POST['nrcpfconjuge'],
                                       nmconjuge = request.POST['nmconjuge']
                                       )
                f_conjuge.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'gleba':gleba,'situacaoprocesso':situacaoprocesso,'caixa':caixa,'municipio':municipio,'tipoprocesso':tipoprocesso, 'processo':escolha, 'div_processo':div_processo}, context_instance = RequestContext(request))    
  
@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/rural/edicao.html',{}, context_instance = RequestContext(request))   

def validacao(request_form):
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
    return warning 
