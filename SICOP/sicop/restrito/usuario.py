from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural, AuthUser, Tbdivisao
from sicop.relatorio_base import relatorio_base_consulta
import datetime
from setuptools._backport.hashlib._sha256 import sha256
from django.contrib.auth.hashers import SHA1PasswordHasher, make_password

#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@login_required
def consulta(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        lista = AuthUser.objects.all().filter( first_name__contains=first_name, email__contains=email )
    else:
        lista = AuthUser.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_usuario'] = lista
    return render_to_response('sicop/restrito/usuario/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    
    divisao = Tbdivisao.objects.all()
    
    ativo = False
    if request.POST.get('is_active',False):
        ativo = True
    
    if request.method == "POST":
        if validacao(request):            
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
def edicao(request, id):
    divisao = Tbdivisao.objects.all()
    
    ativo = False
    if request.POST.get('is_active',False):
        ativo = True
        
    user_obj = get_object_or_404(AuthUser, id=id)
        
    if request.method == "POST":        
        if validacao(request):
            usuario = AuthUser(
                                   id = user_obj.id,
                                   tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                   password = make_password(request.POST['password']),
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
    
    return render_to_response('sicop/restrito/usuario/edicao.html', {'user_obj':user_obj,'divisao':divisao}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_usuario']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS USUARIOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/usuario/consulta/")

def validacao(request_form):
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
    if request_form.POST['password'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a Senha')
        warning = False
    if request_form.POST['tbdivisao'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione a Divisao')
        warning = False
    return warning
