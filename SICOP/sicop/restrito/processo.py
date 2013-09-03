from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula

@login_required
def consulta(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    escolha = "tbprocessorural"
    div_processo = "rural"
    lista = Tbprocessorural.objects.all()
    
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            div_processo = "rural"
            return render_to_response('sicop/restrito/processo/consulta.html',
                    {'tipoprocesso':tipoprocesso,'processo':escolha,
                    'div_processo':div_processo,'lista':lista},
                    context_instance = RequestContext(request));
        else:
            if escolha == "tbprocessourbano":
                div_processo = "urbano"
                lista = Tbprocessourbano.objects.all()
                return render_to_response('sicop/restrito/processo/consulta.html',
                    {'tipoprocesso':tipoprocesso,'processo':escolha,
                    'div_processo':div_processo,'lista':lista},
                    context_instance = RequestContext(request));
            else:
                if escolha == "tbprocessoclausula":
                    div_processo = "clausula"
                    lista = Tbprocessoclausula.objects.all()
                    return render_to_response('sicop/restrito/processo/consulta.html',
                    {'tipoprocesso':tipoprocesso,'processo':escolha,
                    'div_processo':div_processo,'lista':lista},
                    context_instance = RequestContext(request));  
    
    return render_to_response('sicop/restrito/processo/consulta.html',{'tipoprocesso':tipoprocesso,'processo':escolha,'div_processo':div_processo,'lista':lista}, context_instance = RequestContext(request))
   
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    escolha = "tbprocessorural"
    div_processo = "rural"
    form = FormProcessoRural()
        
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            div_processo = "rural"
            form = FormProcessoRural()
            return render_to_response('sicop/restrito/processo/cadastro.html',
                    {"form":form,'tipoprocesso':tipoprocesso,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
        else:
            if escolha == "tbprocessourbano":
                form = FormProcessoUrbano()
                div_processo = "urbano"
                return render_to_response('sicop/restrito/processo/cadastro.html',
                    {"form":form,'tipoprocesso':tipoprocesso,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
            else:
                if escolha == "tbprocessoclausula":
                    form = FormProcessoClausula()
                    div_processo = "clausula"
                    return render_to_response('sicop/restrito/processo/cadastro.html',
                        {"form":form,'tipoprocesso':tipoprocesso,'processo':escolha,
                         'div_processo':div_processo},
                        context_instance = RequestContext(request));  
       
    return render_to_response('sicop/restrito/processo/cadastro.html',{"form":form,'tipoprocesso':tipoprocesso,'processo':escolha,'div_processo':div_processo}, context_instance = RequestContext(request))

