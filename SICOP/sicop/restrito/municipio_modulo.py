from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormProcessos, FormMunicipioModulo
from sicop.models import Tbmunicipiomodulo, Tbmunicipio
from django.contrib import messages
from django.http.response import HttpResponseRedirect

@login_required
def consulta(request):
    municipio = Tbmunicipio.objects.all()
    if request.method == "POST":
        mun = request.POST['tbmunicipio']
        lista = Tbmunicipiomodulo.objects.all()
        if mun != '0':
            lista = lista.filter( tbmunicipio = mun )
    else:
        lista = Tbmunicipiomodulo.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/municipio_modulo/consulta.html' ,{'lista':lista,'municipio':municipio}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    municipio = Tbmunicipio.objects.all()
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
    municipio = Tbmunicipio.objects.all()
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
