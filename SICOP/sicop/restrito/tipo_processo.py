from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoProcesso
from sicop.models import Tbtipoprocesso, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_pdf_base_consulta,\
    relatorio_csv_base_consulta, relatorio_ods_base_consulta

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nome']
        lista = Tbtipoprocesso.objects.all().filter( nome__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_processo'] = lista
    return render_to_response('sicop/restrito/tipo_processo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_tipoprocesso = Tbtipoprocesso(
                                                nome = request.POST['nome'],
                                                tabela = request.POST['tabela'],
                                                coridentificacao = request.POST['coridentificacao'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_tipoprocesso.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_processo/consulta/") 
    return render_to_response('sicop/restrito/tipo_processo/cadastro.html', context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbtipoprocesso, id=id)
    if request.method == "POST":
        if validacao(request):
            f_tipoprocesso = Tbtipoprocesso(
                                                id = instance.id,
                                                nome = request.POST['nome'],
                                                tabela = request.POST['tabela'],
                                                coridentificacao = request.POST['coridentificacao'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_tipoprocesso.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_processo/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/tipo_processo/edicao.html', {"tipoprocesso":instance}, context_instance = RequestContext(request))

def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_tipo_processo']
    if lista:
        resp = relatorio_pdf_base_consulta(request, lista, 'RELATORIO DOS TIPOS DE PROCESSOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/tipo_processo/consulta/")

def relatorio_ods(request):
    return relatorio_ods_base_consulta(request, 
                                       request.session['relatorio_tipo_processo'], 
                                       'RELATORIO DOS TIPOS DE PROCESSOS',
                                       '/sicop/restrito/tipo_processo/consulta/')

def relatorio_csv(request):
    return relatorio_csv_base_consulta(request, 
                                       request.session['relatorio_tipo_processo'], 
                                       'RELATORIO DOS TIPOS DE PROCESSOS',
                                       '/sicop/restrito/tipo_processo/consulta/')

def validacao(request_form):
    warning = True
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo processo')
        warning = False
    if request_form.POST['tabela'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a tabela do tipo processo')
        warning = False
    return warning
