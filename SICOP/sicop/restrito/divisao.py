from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbcaixa, Tbtipocaixa, Tbdivisao, Tbuf
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.forms import FormCaixa, FormDivisao
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmdivisao']
        lista = Tbdivisao.objects.all().filter( nmdivisao__icontains=nome )
    else:
        lista = Tbdivisao.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_divisao'] = lista
    return render_to_response('sicop/restrito/divisao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    
@login_required
def cadastro(request):
    uf = Tbuf.objects.all()
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormDivisao(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/divisao/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormDivisao()
    return render_to_response('sicop/restrito/divisao/cadastro.html',{"form":form,"uf":uf}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    uf = Tbuf.objects.all()
    instance = get_object_or_404(Tbdivisao, id=id)
    if request.method == "POST":
        form = FormDivisao(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/divisao/consulta/")
    else:
        form = FormDivisao(instance=instance)
    return render_to_response('sicop/restrito/divisao/edicao.html', {"form":form,"uf":uf}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_divisao']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS DIVISOES')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/divisao/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmdivisao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da dvisao')
        warning = False
    return warning