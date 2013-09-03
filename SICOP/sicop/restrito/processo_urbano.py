from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.forms import FormProcessoUrbano

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/urbano/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
        
    tipoprocesso = Tbtipoprocesso.objects.all()
    div_processo = "urbano"
    escolha = "tbprocessourbano"
    if request.method == "POST":
        form = FormProcessoUrbano(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
    else:
        form = FormProcessoUrbano() 
           
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'form':form,'tipoprocesso':tipoprocesso,'processo':escolha,
            'div_processo':div_processo}, context_instance = RequestContext(request))    

@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/urbano/edicao.html',{}, context_instance = RequestContext(request))    

def validacao(request_form):
    warning = True
    if request_form.POST['nrcnpj'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CNPJ')
        warning = False
    return warning