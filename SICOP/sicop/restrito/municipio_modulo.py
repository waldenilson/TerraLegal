from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormMunicipioModulo
from sicop.models import Tbmunicipiomodulo, Tbmunicipio, AuthUser
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    if request.method == "POST":
        mun = request.POST['tbmunicipio']
        lista = Tbmunicipiomodulo.objects.all()
        if mun != '0':
            lista = lista.filter( tbmunicipio = mun )
    else:
        lista = Tbmunicipiomodulo.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_municipio_modulo'] = lista
    return render_to_response('sicop/restrito/municipio_modulo/consulta.html' ,{'lista':lista,'municipio':municipio}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    if request.method == "POST":
        form = FormMunicipioModulo(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/municipio_modulo/consulta/") 
    else:
        form = FormMunicipioModulo()
    return render_to_response('sicop/restrito/municipio_modulo/cadastro.html',{"form":form,'municipio':municipio}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    instance = get_object_or_404(Tbmunicipiomodulo, id=id)
    if request.method == "POST":
        form = FormMunicipioModulo(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/municipio_modulo/consulta/")
    else:
        form = FormMunicipioModulo(instance=instance) 
    return render_to_response('sicop/restrito/municipio_modulo/edicao.html', {"form":form,'municipio':municipio}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_municipio_modulo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS MODULOS DOS MUNICIPIOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/municipio_modulo/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nrmodulorural'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do modulo rural')
        warning = False
    if request_form.POST['cdibge'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o codigo ibge')
        warning = False
    if request_form.POST['cdpostal'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o codigo postal')
        warning = False
    if request_form.POST['nrmodulofiscal'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do modulo fiscal')
        warning = False
    if request_form.POST['nrfracaominima'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da fracao minima')
        warning = False
    return warning
