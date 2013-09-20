from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormClassificacaoProcesso
from sicop.models import Tbclassificacaoprocesso
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmclassificacao']
        lista = Tbclassificacaoprocesso.objects.all().filter( nmclassificacao__contains=nome )
    else:
        lista = Tbclassificacaoprocesso.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_classificacao_processo'] = lista
    return render_to_response('sicop/restrito/classificacao_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormClassificacaoProcesso(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/classificacao_processo/consulta/") 
    else:
        form = FormClassificacaoProcesso()
    return render_to_response('sicop/restrito/classificacao_processo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbclassificacaoprocesso, id=id)
    if request.method == "POST":
        form = FormClassificacaoProcesso(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/classificacao_processo/consulta/")
    else:
        form = FormClassificacaoProcesso(instance=instance) 
    return render_to_response('sicop/restrito/classificacao_processo/edicao.html', {"form":form}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_classificacao_processo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS CLASSIFICACOES PROCESSOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/classificacao_processo/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmclassificacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do classificacao processo')
        warning = False
    return warning
