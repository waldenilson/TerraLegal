from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural

#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@login_required
def consulta(request):
    if request.method == "POST":
        requerente = request.POST['requerente']
        cpf = request.POST['cpf']
        entrega = request.POST['entrega']
        lista = Tbpecastecnicas.objects.all().filter( nmrequerente__contains=requerente, nrcpfrequerente__contains=cpf, nrentrega__contains=entrega )
    else:
        lista = Tbpecastecnicas.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/peca_tecnica/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
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
            peca = Tbpecastecnicas(
                                   tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                   tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                   tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                   nrarea = request.POST['nrarea'],
                                   nrperimetro = request.POST['nrperimetro'],
                                   dsobservacao = request.POST['dsobservacao'],
                                   nrentrega = request.POST['nrentrega'],
                                   nmrequerente = request.POST['nmrequerente'],
                                   nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                   stanexadoprocesso = anexadoprocesso,
                                   stpecatecnica = pecatecnica,
                                   stenviadobrasilia = enviadobrasilia
                                   )
            peca.save()
            return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/") 
    
    return render_to_response('sicop/restrito/peca_tecnica/cadastro.html',{'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))


@login_required
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
            peca = Tbpecastecnicas(
                                   id = peca_obj.id,
                                   tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                   tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                   tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                   nrarea = request.POST['nrarea'],
                                   nrperimetro = request.POST['nrperimetro'],
                                   dsobservacao = request.POST['dsobservacao'],
                                   nrentrega = request.POST['nrentrega'],
                                   nmrequerente = request.POST['nmrequerente'],
                                   nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                   stanexadoprocesso = anexadoprocesso,
                                   stpecatecnica = pecatecnica,
                                   stenviadobrasilia = enviadobrasilia
                                   )
            peca.save()
            return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/")

    processo = Tbprocessorural.objects.all().filter( nrcpfrequerente = peca_obj.nrcpfrequerente.replace('.','').replace('-','') )
    return render_to_response('sicop/restrito/peca_tecnica/edicao.html',
                              {'peca':peca_obj,'processo':processo,'caixa':caixa,'contrato':contrato,'gleba':gleba}, 
                            context_instance = RequestContext(request))

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
    if request_form.POST['nrarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da area')
        warning = False
    if request_form.POST['nrperimetro'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do perimetro')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione uma Gleba') 
        warning = False
    return warning
