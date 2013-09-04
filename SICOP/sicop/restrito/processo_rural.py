from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect

@login_required
def consulta(request):
    return render_to_response('sicop/restrito/processo/rural/consulta.html',{}, context_instance = RequestContext(request))    
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    div_processo = "rural"
    escolha = "tbprocessorural"
    form_rural = FormProcessoRural() 
    form_base = FormProcessoBase()
    
    if request.method == "POST":
        if validacao(request):
            # preencher forms base e rural com os requests
            form_rural.nmrequerente = request.POST['nmrequerente']
            form_rural.nrcpfrequerente = request.POST['nrcpfrequerente']
            
            if form_rural.is_valid() and form_base.is_valid():
                form_base_new = form_base.save()
                form_rural.tbprocessobase = form_base_new.pk
                form_rural.save()
                return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso, 'processo':escolha, 'div_processo':div_processo}, context_instance = RequestContext(request))    
  
@login_required
def edicao(request):
    return render_to_response('sicop/restrito/processo/rural/edicao.html',{}, context_instance = RequestContext(request))   

def validacao(request_form):
    warning = True
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do requerente')
        warning = False
    return warning 
