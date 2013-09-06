from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula

@login_required
def consulta(request):
    lista = Tbprocessobase.objects.all()
    if request.method == "POST":
        escolha = request.POST['escolha']
        pesquisa = request.POST['pesquisa']
        if escolha == "numero":
            lista = Tbprocessobase.objects.all().filter( nrprocesso__contains = pesquisa )
        else:
            if escolha == "nome":
                p_rural = Tbprocessorural.objects.all().filter( nmrequerente__contains = pesquisa )
                p_clausula = Tbprocessoclausula.objects.all().filter( nmrequerente__contains = pesquisa )
                lista = []
                for obj in p_rural:
                    lista.append( obj.tbprocessobase )
                for obj in p_clausula:
                    lista.append( obj.tbprocessobase )
            else:
                if escolha == "cpf":
                    p_rural = Tbprocessorural.objects.all().filter( nrcpfrequerente__contains = pesquisa )
                    p_clausula = Tbprocessoclausula.objects.all().filter( nrcpfrequerente__contains = pesquisa )
                    lista = []
                    for obj in p_rural:
                        lista.append( obj.tbprocessobase )
                    for obj in p_clausula:
                        lista.append( obj.tbprocessobase )
                else:
                    if escolha == "cnpj":
                        p_urbano = Tbprocessourbano.objects.all().filter( nrcnpj__contains = pesquisa ) 
                        lista = []
                        for obj in p_urbano:
                            lista.append( obj.tbprocessobase )
        
    return render_to_response('sicop/restrito/processo/consulta.html',{'lista':lista}, context_instance = RequestContext(request))
   
    
@login_required
@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    escolha = "tbprocessorural"
    div_processo = "rural"
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    municipio = Tbmunicipio.objects.all()
    contrato = Tbcontrato.objects.all()
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
            
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            div_processo = "rural"
            return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
        else:
            if escolha == "tbprocessourbano":
                div_processo = "urbano"
                return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo,'contrato':contrato},
                    context_instance = RequestContext(request));  
            else:
                if escolha == "tbprocessoclausula":
                    div_processo = "clausula"
                    return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
       
    return render_to_response('sicop/restrito/processo/cadastro.html',{'gleba':gleba,'caixa':caixa,'municipio':municipio,'situacaoprocesso':situacaoprocesso,
            'tipoprocesso':tipoprocesso,'processo':escolha,'div_processo':div_processo}, context_instance = RequestContext(request))

