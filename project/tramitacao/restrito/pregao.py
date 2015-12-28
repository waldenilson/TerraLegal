from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import PregaoForm
from project.tramitacao.models import Tbpregao, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse

@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        lista = Tbpregao.objects.filter( nrpregao__icontains=request.POST['nrpregao'], dspregao__contains=request.POST['dspregao'], tbdivisao__id__in = request.session['divisoes']).order_by('nrpregao') #AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbpregao.objects.filter( tbdivisao__id__in = request.session['divisoes']).order_by('nrpregao')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    return render_to_response('sicop/pregao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.pregao_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    form = PregaoForm()
    if request.method == "POST":
        form = PregaoForm(request.POST)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/pregao/cadastro.html',{'form':form},context_instance = RequestContext(request))

@permission_required('sicop.pregao_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    obj = get_object_or_404(Tbpregao, id=id)
    form = PregaoForm(instance=obj)
    if request.method == "POST":
        if not request.user.has_perm('sicop.pregao_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = PregaoForm(request.POST, instance=obj)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/pregao/cadastro.html',{'form':form},context_instance = RequestContext(request))

def form_save(request, form):
    form.tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
    form.save()
    return HttpResponseRedirect( '/tramitacao/pregao/consulta' )