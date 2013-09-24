from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSubArea
from sicop.models import Tbsubarea
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nmsubarea']
        lista = Tbsubarea.objects.all().filter( nmsubarea__contains=num )
    else:
        lista = Tbsubarea.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_sub_area'] = lista
    return render_to_response('sicop/restrito/sub_area/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormSubArea(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormSubArea()
    return render_to_response('sicop/restrito/sub_area/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbsubarea, id=id)
    if request.method == "POST":
        form = FormSubArea(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")
    else:
        form = FormSubArea(instance=instance)
    return render_to_response('sicop/restrito/sub_area/edicao.html', {"form":form}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_sub_area']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS SUB AREAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmsubarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a sub area')
        warning = False
    return warning