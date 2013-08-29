#PROCESSOS -----------------------------------------------------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from newsicop.forms import FormProcessos

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/consulta.html',{}, 
                              context_instance = RequestContext(request))    
    
@login_required
@permission_required('web.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    form = FormProcessos()
    return render_to_response('sicop/restrito/processo/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/edicao.html',{})
