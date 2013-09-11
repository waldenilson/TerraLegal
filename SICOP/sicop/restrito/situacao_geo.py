from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSituacaoProcesso, FormSituacaoGeo
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.models import Tbsituacaoprocesso, Tbsituacaogeo

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmsituacaogeo']
        lista = Tbsituacaogeo.objects.all().filter( nmsituacaogeo__contains=nome )
    else:
        lista = Tbsituacaogeo.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/situacao_geo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormSituacaoGeo(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/situacao_geo/consulta/") 
    else:
        form = FormSituacaoGeo()
    return render_to_response('sicop/restrito/situacao_geo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbsituacaogeo, id=id)
    if request.method == "POST":
        form = FormSituacaoGeo(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/situacao_geo/consulta/")
    else:
        form = FormSituacaoGeo(instance=instance) 
    return render_to_response('sicop/restrito/situacao_geo/edicao.html', {"form":form}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['nmsituacaogeo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da situacao geo')
        warning = False
    return warning