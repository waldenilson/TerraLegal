from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormStatusPendencia
from sicop.models import Tbstatuspendencia, AuthUser
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['dspendencia']
        lista = Tbstatuspendencia.objects.all().filter( dspendencia__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbstatuspendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_status_pendencia'] = lista
    return render_to_response('sicop/restrito/status_pendencia/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        if validacao(request):
            f_statuspendencia = Tbstatuspendencia(
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_statuspendencia.save()
            return HttpResponseRedirect("/sicop/restrito/status_pendencia/consulta/") 
    return render_to_response('sicop/restrito/status_pendencia/cadastro.html',{}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbstatuspendencia, id=id)
    if request.method == "POST":
        if validacao(request):
            f_statuspendencia = Tbstatuspendencia(
                                        id = instance.id,
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_statuspendencia.save()
            return HttpResponseRedirect("/sicop/restrito/status_pendencia/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/status_pendencia/edicao.html', {"statuspendencia":instance}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_status_pendencia']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS STATUS PENDENCIA')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/status_pendencia/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['dspendencia'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do status pendencia')
        warning = False
    return warning
