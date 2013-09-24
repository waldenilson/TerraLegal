from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormGleba
from sicop.models import Tbgleba, Tbsubarea
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmgleba']
        lista = Tbgleba.objects.all().filter( nmgleba__contains=nome )
    else:
        lista = Tbgleba.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_gleba'] = lista
    return render_to_response('sicop/restrito/gleba/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    subarea = Tbsubarea.objects.all()
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormGleba(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormGleba()
    return render_to_response('sicop/restrito/gleba/cadastro.html',{"form":form,'subarea':subarea}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    subarea = Tbsubarea.objects.all()
    instance = get_object_or_404(Tbgleba, id=id)
    if request.method == "POST":
        form = FormGleba(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")
    else:
        form = FormGleba(instance=instance) 
    return render_to_response('sicop/restrito/gleba/edicao.html', {"form":form,'subarea':subarea}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_gleba']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS GLEBAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da gleba')
        warning = False
    return warning
