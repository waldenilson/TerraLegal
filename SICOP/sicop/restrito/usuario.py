from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural, AuthUser, Tbdivisao, AuthGroup,\
    AuthUserGroups
from sicop.relatorio_base import relatorio_base_consulta
import datetime
from django.contrib.auth.hashers import make_password, load_hashers, get_hasher
import json
from collections import OrderedDict
from sicop.admin import verificar_permissao_grupo

#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def consulta(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        print 'User: '+AuthUser.objects.get( pk = request.user.id ).tbdivisao.nmdivisao
        # se usuario for do grupo Super; mostra todos senao mostra somente os usuarios da divisao
        if verificar_permissao_grupo( AuthUser.objects.get( pk = request.user.id ), {'Super'} ):
            lista = AuthUser.objects.all().filter( first_name__icontains=first_name, email__icontains=email )
        else:
            lista = AuthUser.objects.all().filter( first_name__icontains=first_name, email__icontains=email, 
                                                   tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        # se usuario for do grupo Super; mostra todos senao mostra somente os usuarios da divisao
        if verificar_permissao_grupo( AuthUser.objects.get( pk = request.user.id ), {'Super'} ):
            lista = AuthUser.objects.all()
        else:
            lista = AuthUser.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )

    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_usuario'] = lista
    return render_to_response('sicop/restrito/usuario/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    
    divisao = Tbdivisao.objects.all()
    
    ativo = False
    if request.POST.get('is_active',False):
        ativo = True
    
    if request.method == "POST":
        if validacao(request, 'cadastro'):            
            usuario = AuthUser(
                                   tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                   password = make_password(request.POST['password']),
                                   first_name = request.POST['first_name'],
                                   last_name = request.POST['last_name'],
                                   email = request.POST['email'],
                                   username = request.POST['username'],
                                   is_superuser = True,
                                   is_staff = True,
                                   is_active = ativo,
                                   last_login = datetime.datetime.now(),
                                   date_joined = datetime.datetime.now()
                                   )
            usuario.save()
            return HttpResponseRedirect("/sicop/restrito/usuario/consulta/") 
    
    return render_to_response('sicop/restrito/usuario/cadastro.html',{'divisao':divisao}, context_instance = RequestContext(request))


@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    divisao = Tbdivisao.objects.all()
    grupo = AuthGroup.objects.all()
    userGrupo = AuthUserGroups.objects.all().filter( user = id )
    
    result = {}
    for obj in grupo:
        achou = False
        for obj2 in userGrupo:
            if obj.id == obj2.group.id:
                result.setdefault(obj.name,True)
                achou = True
                break
        if not achou:
            result.setdefault(obj.name, False)
    result = sorted(result.items())
    
    ativo = False
    if request.POST.get('is_active',False):
        ativo = True
        
    user_obj = get_object_or_404(AuthUser, id=id)

    if request.method == "POST":
        
        # verificando os grupos do usuario
        for obj in grupo:
            if request.POST.get(obj.name, False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                if not res:
                    # inserir ao authusergroups
                    ug = AuthUserGroups( user = AuthUser.objects.get( pk = id ),
                                          group = AuthGroup.objects.get( pk = obj.id ) )
                    ug.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                if res:
                    # excluir do authusergroups
                    for aug in res:
                        aug.delete()
                    #print obj.name + ' desmarcou deste usuario'
                    
        if validacao(request, 'edicao'):
            
            # tratar o campo senha
            senha_digitada = request.POST['password']
            senha_atual = user_obj.password
            if len(senha_digitada) > 2:
                senha_atual = make_password( senha_digitada )
            
            usuario = AuthUser(
                                   id = user_obj.id,
                                   tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                   password = senha_atual,
                                   first_name = request.POST['first_name'],
                                   last_name = request.POST['last_name'],
                                   email = request.POST['email'],
                                   username = request.POST['username'],
                                   is_superuser = True,
                                   is_staff = True,
                                   is_active = ativo,
                                   last_login = user_obj.last_login,
                                   date_joined = user_obj.date_joined
                                   )
            usuario.save()
            return HttpResponseRedirect("/sicop/restrito/usuario/consulta/")
    
    return render_to_response('sicop/restrito/usuario/edicao.html', 
                              {'result':result,'grupo':grupo,'usergrupo':userGrupo,'user_obj':user_obj,'divisao':divisao}, context_instance = RequestContext(request))

    
def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_usuario']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS USUARIOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/usuario/consulta/")

def validacao(request_form, acao):
    warning = True
    if request_form.POST['first_name'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Nome')
        warning = False
    if request_form.POST['last_name'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Sobrenome')
        warning = False
    if request_form.POST['username'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Login')
        warning = False
    if acao == 'cadastro':
        if request_form.POST['password'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe a Senha')
            warning = False
    if request_form.POST['tbdivisao'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione a Divisao')
        warning = False
    return warning
