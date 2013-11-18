from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormStatusPendencia, FormAuthGroup
from sicop.models import Tbstatuspendencia, AuthGroup
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def consulta(request):
    if request.method == "POST":
        nome = request.POST['name']
        lista = AuthGroup.objects.all().filter( name__icontains=nome )
    else:
        lista = AuthGroup.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_grupo'] = lista
    return render_to_response('sicop/restrito/grupo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        form = FormAuthGroup(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/grupo/consulta/") 
    else:
        form = FormAuthGroup()
    return render_to_response('sicop/restrito/grupo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(AuthGroup, id=id)
    if request.method == "POST":
        form = FormAuthGroup(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/grupo/consulta/")
    else:
        form = FormAuthGroup(instance=instance) 
    return render_to_response('sicop/restrito/grupo/edicao.html', {"form":form}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_grupo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS GRUPOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/grupo/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['name'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do grupo')
        warning = False
    return warning
