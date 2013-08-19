# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response, get_object_or_404
from web.models import Tbcaixa, Tbtipocaixa, Tbpecastecnicas
from web.forms import FormPecasTecnicas, FormProcessos
from django.http import request

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
        print requerente
        lista = Tbpecastecnicas.objects.filter( nmrequerente__contains=requerente ).order_by('id')
    else:
        lista = Tbpecastecnicas.objects.all()
    return render_to_response('sicop/pecas_tecnicas.html',{'lista_peca_tecnica':lista}, context_instance = RequestContext(request))

@login_required
def pecas_tecnicas_novo(request):
    form = FormPecasTecnicas()
    return render_to_response('sicop/pecas_tecnicas_novo.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def pecas_tecnicas_edicao(request):
    if request.method == "GET":
        id_consulta = request.GET['id']
        print id_consulta
        objPeca = get_object_or_404(Tbpecastecnicas, pk=id_consulta)

    return render_to_response('sicop/pecas_tecnicas_edicao.html',{"obj_peca":objPeca})


#RELATORIOS -----------------------------------------------------------------------------------------------------------------------------



@login_required
def relatorios(request):
    return render_to_response('sicop/relatorios.html',{})

