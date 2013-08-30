from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormProcessos, FormSituacaoProcessoUrbano
from sicop.models import Tbsituacaoprocessourbano
from django.contrib import messages
from django.http.response import HttpResponseRedirect

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmsituacao']
        lista = Tbsituacaoprocessourbano.objects.all().filter( nmsituacao__contains=nome )
    else:
        lista = Tbsituacaoprocessourbano.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/situacao_processo_urbano/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormSituacaoProcessoUrbano(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/situacao_processo_urbano/consulta/") 
    else:
        form = FormSituacaoProcessoUrbano()
    return render_to_response('sicop/restrito/situacao_processo_urbano/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbsituacaoprocessourbano, id=id)
    if request.method == "POST":
        form = FormSituacaoProcessoUrbano(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/situacao_processo_urbano/consulta/")
    else:
        form = FormSituacaoProcessoUrbano(instance=instance) 
    return render_to_response('sicop/restrito/situacao_processo_urbano/edicao.html', {"form":form}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['nmsituacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da situacao processo urbano')
        warning = False
    return warning
