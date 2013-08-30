from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormProcessos, FormContrato
from django.contrib import messages
from sicop.models import Tbcontrato
from django.http.response import HttpResponseRedirect

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nrcontrato']
        nome = request.POST['nmempresa']
        lista = Tbcontrato.objects.all().filter( nrcontrato__contains=num, nmempresa__contains=nome )
    else:
        lista = Tbcontrato.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/contrato/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormContrato(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/contrato/consulta/") 
    else:
        form = FormContrato()
    return render_to_response('sicop/restrito/contrato/cadastro.html',{"form":form}, context_instance = RequestContext(request))
@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbcontrato, id=id)
    if request.method == "POST":
        form = FormContrato(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/contrato/consulta/")
    else:
        form = FormContrato(instance=instance) 
    return render_to_response('sicop/restrito/contrato/edicao.html', {"form":form}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['nrcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do contrato')
        warning = False
    if request_form.POST['nmempresa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da empresa')
        warning = False
    return warning
