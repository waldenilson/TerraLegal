from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.tramitacao.forms import SubAreaForm
from TerraLegal.tramitacao.models import Tbsubarea, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse

@permission_required('sicop.sub_area_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        lista = Tbsubarea.objects.filter( nmsubarea__icontains=request.POST['nmsubarea'], tbdivisao__id__in = request.session['divisoes']).order_by('nmsubarea') #AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbsubarea.objects.filter( tbdivisao__id__in = request.session['divisoes']).order_by('nmsubarea')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    return render_to_response('sicop/sub_area/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.sub_area_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    form = SubAreaForm()
    if request.method == "POST":
        form = SubAreaForm(request.POST)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/sub_area/cadastro.html',{'form':form},context_instance = RequestContext(request))

@permission_required('sicop.sub_area_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    obj = get_object_or_404(Tbsubarea, id=id)
    form = SubAreaForm(instance=obj)
    if request.method == "POST":
        if not request.user.has_perm('sicop.sub_area_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        form = SubAreaForm(request.POST, instance=obj)
        if form.is_valid():
            return form_save(request, form)
    return render_to_response('sicop/sub_area/cadastro.html',{'form':form},context_instance = RequestContext(request))

def form_save(request, form):
    form.tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
    form.save()
    return HttpResponseRedirect( '/sicop/sub_area/consulta' )