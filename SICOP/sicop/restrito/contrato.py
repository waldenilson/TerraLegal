from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormContrato
from django.contrib import messages
from sicop.models import Tbcontrato, AuthUser
from django.http.response import HttpResponseRedirect
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nrcontrato']
        nome = request.POST['nmempresa']
        lista = Tbcontrato.objects.all().filter( nrcontrato__icontains=num, nmempresa__contains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbcontrato.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_contrato'] = lista
    return render_to_response('sicop/restrito/contrato/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_contrato = Tbcontrato(
                                        nrcontrato = request.POST['nrcontrato'],
                                        nmempresa = request.POST['nmempresa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_contrato.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/contrato/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/contrato/cadastro.html',
                               context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbcontrato, id=id)
    if request.method == "POST":
        if validacao(request):
            f_contrato = Tbcontrato(
                                        id = instance.id,
                                        nrcontrato = request.POST['nrcontrato'],
                                        nmempresa = request.POST['nmempresa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_contrato.save()
            return HttpResponseRedirect("/sicop/restrito/contrato/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/contrato/edicao.html', {"contrato":instance}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_contrato']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS CONTRATOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/contrato/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nrcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do contrato')
        warning = False
    if request_form.POST['nmempresa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da empresa')
        warning = False
    return warning
