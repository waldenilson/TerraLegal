from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbcaixa, Tbtipocaixa
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.forms import FormCaixa

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmlocalarquivo']
        lista = Tbcaixa.objects.all().filter( nmlocalarquivo__contains=nome )
    else:
        lista = Tbcaixa.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
def cadastro(request):
    tipocaixa = Tbtipocaixa.objects.all()
    if request.method == "POST":
        form = FormCaixa(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/caixa/consulta/") 
    else:
        form = FormCaixa()
    return render_to_response('sicop/restrito/caixa/cadastro.html',{"form":form,"tipocaixa":tipocaixa}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    tipocaixa = Tbtipocaixa.objects.all()
    instance = get_object_or_404(Tbcaixa, id=id)
    if request.method == "POST":
        form = FormCaixa(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/caixa/consulta/")
    else:
        form = FormCaixa(instance=instance)
    return render_to_response('sicop/restrito/caixa/edicao.html', {"form":form,"tipocaixa":tipocaixa}, context_instance = RequestContext(request))


def validacao(request_form):
    warning = True
    if request_form.POST['nmlocalarquivo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a caixa')
        warning = False
    return warning