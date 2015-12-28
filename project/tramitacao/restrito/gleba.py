#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import GlebaForm
from project.tramitacao.models import Tbgleba, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse

@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        lista = Tbgleba.objects.filter( nmgleba__icontains=request.POST['nmgleba']).order_by('nmgleba')
    else:
        lista = Tbgleba.objects.all().order_by('nmgleba')
    return render_to_response('sicop/gleba/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.gleba_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    form = GlebaForm()
    if request.method == "POST":
        form = GlebaForm(request.POST)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/gleba/cadastro.html',{'form':form},context_instance = RequestContext(request))

@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    obj = get_object_or_404(Tbgleba, id=id)
    form = GlebaForm(instance=obj)
    if request.method == "POST":
        if not request.user.has_perm('sicop.gleba_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = GlebaForm(request.POST, instance=obj)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/gleba/cadastro.html',{'form':form},context_instance = RequestContext(request))

def form_save(request, form):
    form.save()
    return HttpResponseRedirect( '/sicop/gleba/consulta' )