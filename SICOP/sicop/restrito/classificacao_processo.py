from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormClassificacaoProcesso
from sicop.models import Tbclassificacaoprocesso, AuthUser
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmclassificacao']
        lista = Tbclassificacaoprocesso.objects.all().filter( nmclassificacao__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbclassificacaoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_classificacao_processo'] = lista
    return render_to_response('sicop/restrito/classificacao_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_classificacao = Tbclassificacaoprocesso(
                                                        nmclassificacao = request.POST['nmclassificacao'],
                                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                                      )
            f_classificacao.save()
            return HttpResponseRedirect("/sicop/restrito/classificacao_processo/consulta/") 
    return render_to_response('sicop/restrito/classificacao_processo/cadastro.html', context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbclassificacaoprocesso, id=id)
    if request.method == "POST":
        if validacao(request):
            f_classificacao = Tbclassificacaoprocesso(
                                                        id = instance.id,
                                                        nmclassificacao = request.POST['nmclassificacao'],
                                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                                      )
            f_classificacao.save()
            return HttpResponseRedirect("/sicop/restrito/classificacao_processo/consulta/")
    return render_to_response('sicop/restrito/classificacao_processo/edicao.html', {"classificacao":instance}, context_instance = RequestContext(request))

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
