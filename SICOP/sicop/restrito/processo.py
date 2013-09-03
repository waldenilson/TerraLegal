from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso
from django.http.response import HttpResponseRedirect

@login_required
def consulta(request):
    escolha = "0"
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            return HttpResponseRedirect("/sicop/restrito/processo/rural/consulta/")
        else:
            if escolha == "tbprocessourbano":
                return HttpResponseRedirect("/sicop/restrito/processo/urbano/consulta/")
            else:
                if escolha == "tbprocessoclausula":
                    return HttpResponseRedirect("/sicop/restrito/processo/clausula/consulta/")
    
    tipoprocesso = Tbtipoprocesso.objects.all()
    return render_to_response('sicop/restrito/processo/consulta.html',{'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))
   
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    escolha = "0"
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            return HttpResponseRedirect("/sicop/restrito/processo/rural/cadastro/")
        else:
            if escolha == "tbprocessourbano":
                return HttpResponseRedirect("/sicop/restrito/processo/urbano/cadastro/")
            else:
                if escolha == "tbprocessoclausula":
                    return HttpResponseRedirect("/sicop/restrito/processo/clausula/cadastro/")
    
    tipoprocesso = Tbtipoprocesso.objects.all()
    return render_to_response('sicop/restrito/processo/cadastro.html',{'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))

