from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import TipoCaixaForm
from project.tramitacao.models import Tbtipocaixa, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse

@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        lista = Tbtipocaixa.objects.filter( nmtipocaixa__icontains=request.POST['nmtipocaixa']).order_by('nmtipocaixa')
    else:
        lista = Tbtipocaixa.objects.all().order_by('nmtipocaixa')
    return render_to_response('sicop/tipo_caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.tipo_caixa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    form = TipoCaixaForm()
    if request.method == "POST":
        form = TipoCaixaForm(request.POST)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/tipo_caixa/cadastro.html',{'form':form},context_instance = RequestContext(request))

@permission_required('sicop.tipo_caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    obj = get_object_or_404(Tbtipocaixa, id=id)
    form = TipoCaixaForm(instance=obj)
    if request.method == "POST":
        if not request.user.has_perm('sicop.tipo_caixa_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = TipoCaixaForm(request.POST, instance=obj)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/tipo_caixa/cadastro.html',{'form':form},context_instance = RequestContext(request))

def form_save(request, form):
    form.save()
    return HttpResponseRedirect( '/tramitacao/tipo_caixa/consulta' )