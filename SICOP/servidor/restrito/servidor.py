from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato

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
    
    # combobox
    gleba = Tbgleba.objects.all()
    # buscar caixa do tipo peca
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    contrato = Tbcontrato.objects.all()
    
    return render_to_response('sicop/restrito/peca_tecnica/consulta.html' ,{'lista_peca_tecnica':lista,'gleba':gleba,'contrato':contrato,'caixa':caixa}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    gleba = Tbgleba.objects.all()
    
    if request.method == "POST":
        form = FormPecasTecnicas(request.POST)
        form.tbcaixa = request.POST['tbcaixa']
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/") 
    else:
        form = FormPecasTecnicas()
    
    return render_to_response('sicop/restrito/peca_tecnica/cadastro.html',{"form":form,'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    gleba = Tbgleba.objects.all()
    
    instance = get_object_or_404(Tbpecastecnicas, id=id)
        
    if request.method == "POST":
        form = FormPecasTecnicas(request.POST,request.FILES,instance=instance)
        
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/peca_tecnica/consulta/")
    #else:
     #   id_consulta = id_peca
      #  objPeca = get_object_or_404(Tbpecastecnicas, pk=id_consulta)
    else:
        form = FormPecasTecnicas(instance=instance) 

    return render_to_response('sicop/restrito/peca_tecnica/edicao.html',
                              {"form":form,'caixa':caixa,'contrato':contrato,'gleba':gleba}, 
                              context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['tbcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione um Contrato')
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
