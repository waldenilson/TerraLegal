# Create your views here.
from django.template import loader
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response, get_object_or_404
from web.models import Tbcaixa, Tbtipocaixa, Tbpecastecnicas, Tbgleba,\
    Tbcontrato
from web.forms import FormPecasTecnicas, FormProcessos
from django.http import request
from web.validacao import validacao_form_peca_tecnica
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.core import paginator, serializers

@login_required
def acesso_restrito(request):
    return render_to_response('sicop/acesso_restrito.html')    
    

#PROCESSOS -----------------------------------------------------------------------------------------------------------------------------


@login_required
def processos(request):
    if request.method == "POST":
        retorno = request.POST['query']
    else:
        retorno = ''
    lista = Tbtipocaixa.objects.filter( nmtipocaixa__contains=retorno ).order_by('id')
    return render_to_response('sicop/processos.html',{'lista':lista,'retorno':retorno}, 
                              context_instance = RequestContext(request))    
    
@login_required
@permission_required('web.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def processos_novo(request):
    form = FormProcessos()
    return render_to_response('sicop/processos_novo.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def processos_edicao(request):
    return render_to_response('sicop/processos_edicao.html',{})


#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@login_required
def pecas_tecnicas(request):
    
    if request.method == "POST":
        requerente = request.POST['requerente']
        cpf = request.POST['cpf']
        entrega = request.POST['entrega']
        contrato = request.POST['contrato']
        gleba = request.POST['gleba']
        caixa = request.POST['caixa']
        lista = Tbpecastecnicas.objects.all().filter( nmrequerente__contains=requerente, nrcpfrequerente__contains=cpf, nrentrega__contains=entrega )
        if contrato != '0':
            lista = lista.filter( tbcontrato=contrato )
        if gleba != '0':
            lista = lista.filter( tbgleba=gleba )
        if caixa != '0':
            lista = lista.filter( tbcaixa=caixa )
    
    else:
        lista = Tbpecastecnicas.objects.all()
    
    # combobox
    gleba = Tbgleba.objects.all()
    # buscar caixa do tipo peca
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    contrato = Tbcontrato.objects.all()
    
    return render_to_response('sicop/pecas_tecnicas.html',{'lista_peca_tecnica':lista,'gleba':gleba,'contrato':contrato,'caixa':caixa}, context_instance = RequestContext(request))

@login_required
def pecas_tecnicas_novo(request):
    
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    gleba = Tbgleba.objects.all()
    
    if request.method == "POST":
        form = FormPecasTecnicas(request.POST)
        form.tbcaixa = request.POST['tbcaixa']
        if validacao_form_peca_tecnica(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/pecas_tecnicas/") 
    else:
        form = FormPecasTecnicas()
    
    return render_to_response('sicop/pecas_tecnicas_novo.html',{"form":form,'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))

@login_required
def pecas_tecnicas_edicao(request, id_peca):
    
    contrato = Tbcontrato.objects.all()
    caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    gleba = Tbgleba.objects.all()
    
    if request.method == "POST":
        form = FormPecasTecnicas(request.POST)
        form.tbcaixa = request.POST['tbcaixa']
        if validacao_form_peca_tecnica(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/pecas_tecnicas/") 
    else:
        id_consulta = id_peca
        objPeca = get_object_or_404(Tbpecastecnicas, pk=id_consulta)

    return render_to_response('sicop/pecas_tecnicas_edicao.html',{"obj_peca":objPeca,'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))


#RELATORIOS -----------------------------------------------------------------------------------------------------------------------------



@login_required
def relatorios(request):
    return render_to_response('sicop/relatorios.html',{})

