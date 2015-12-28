from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import ContratoForm
from project.tramitacao.models import Tbcontrato, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        lista = Tbcontrato.objects.filter( nrcontrato__icontains=request.POST['nrcontrato'], nmempresa__contains=request.POST['nmempresa'], tbdivisao__id__in = request.session['divisoes']).order_by('nmempresa') #AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbcontrato.objects.filter( tbdivisao__id__in = request.session['divisoes']).order_by('nmempresa')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    return render_to_response('sicop/contrato/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.contrato_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    form = ContratoForm()
    if request.method == "POST":
        form = ContratoForm(request.POST)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/contrato/cadastro.html',{'form':form},context_instance = RequestContext(request))

@permission_required('sicop.contrato_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    obj = get_object_or_404(Tbcontrato, id=id)
    form = ContratoForm(instance=obj)
    if request.method == "POST":
        if not request.user.has_perm('sicop.contrato_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = ContratoForm(request.POST, instance=obj)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/contrato/cadastro.html',{'form':form},context_instance = RequestContext(request))

def form_save(request, form):
    form.tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
    form.save()
    return HttpResponseRedirect( '/tramitacao/contrato/consulta' )