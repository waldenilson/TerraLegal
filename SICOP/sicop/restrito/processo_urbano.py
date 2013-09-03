from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/urbano/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    return render_to_response('sicop/restrito/processo/urbano/cadastro.html',{}, context_instance = RequestContext(request))    

@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/urbano/edicao.html',{}, context_instance = RequestContext(request))    
