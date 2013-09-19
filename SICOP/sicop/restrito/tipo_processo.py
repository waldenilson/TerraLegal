from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoProcesso
from sicop.models import Tbtipoprocesso
from django.http.response import HttpResponseRedirect
from django.contrib import messages

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nome']
        lista = Tbtipoprocesso.objects.all().filter( nome__contains=nome )
    else:
        lista = Tbtipoprocesso.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_processo'] = lista
    return render_to_response('sicop/restrito/tipo_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormTipoProcesso(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/tipo_processo/consulta/") 
    else:
        form = FormTipoProcesso()
    return render_to_response('sicop/restrito/tipo_processo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbtipoprocesso, id=id)
    if request.method == "POST":
        form = FormTipoProcesso(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/tipo_processo/consulta/")
    else:
        form = FormTipoProcesso(instance=instance) 
    return render_to_response('sicop/restrito/tipo_processo/edicao.html', {"form":form}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo processo')
        warning = False
    if request_form.POST['tabela'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a tabela do tipo processo')
        warning = False
    return warning
