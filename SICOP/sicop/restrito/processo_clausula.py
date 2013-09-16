from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbmunicipio, Tbgleba, Tbcaixa,\
    Tbprocessobase, AuthUser, Tbprocessoclausula, Tbclassificacaoprocesso,\
    Tbsituacaoprocesso
from sicop.forms import FormProcessoClausula
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/clausula/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    municipio = Tbmunicipio.objects.all()
    
    procuracao = False
    if request.POST.get('stprocuracao',False):
        procuracao = True
        
    div_processo = "clausula"
    escolha = "tbprocessoclausula"  
    
    if request.method == "POST":
        if validacao(request):
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessoclausula' ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo rural
            f_clausula = Tbprocessoclausula (
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nminteressado = request.POST['nminteressado'],
                                       nrcpfinteressado = request.POST['nrcpfinteressado'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       dttitulacao =  datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y"),
                                       nrarea = request.POST['nrarea'],
                                       stprocuracao = procuracao,
                                       tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                       dsobs = request.POST['dsobs']
                                       )
            f_clausula.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
    
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'processo':escolha, 'gleba':gleba,'caixa':caixa,'municipio':municipio,'div_processo':div_processo},
         context_instance = RequestContext(request))     

@login_required
def edicao(request, id):
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    municipio = Tbmunicipio.objects.all()
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    
    procuracao = False
    if request.POST.get('stprocuracao',False):
        procuracao = True
    
    clausula = get_object_or_404(Tbprocessoclausula, id=id)
    base  = get_object_or_404(Tbprocessobase, id=clausula.tbprocessobase.id)
    
    if validacao(request):
        # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessoclausula' ),
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id )
                                    )
            f_base.save()
            
            # cadastrando o registro processo clausula
            f_clausula = Tbprocessoclausula (
                                       id = clausula.id,
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nminteressado = request.POST['nminteressado'],
                                       nrcpfinteressado = request.POST['nrcpfinteressado'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       dttitulacao =  datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y"),
                                       nrarea = request.POST['nrarea'],
                                       stprocuracao = procuracao,
                                       tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                       dsobs = request.POST['dsobs']
                                       )
            f_clausula.save()
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,
                                   'base':base,'clausula':clausula}, context_instance = RequestContext(request))    

def validacao(request_form):
    warning = True
    if request_form.POST['nrprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
        warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do titulado')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CPF do titulado')
        warning = False
    if request_form.POST['nminteressado'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do Interessado')
        warning = False
    if request_form.POST['nrcpfinteressado'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CPF do interessado')
        warning = False
    if request_form.POST['tbcaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
        warning = False
    if request_form.POST['nrarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da area')
        warning = False
    if request_form.POST['dttitulacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a data de titulacao')
        warning = False
    return warning
