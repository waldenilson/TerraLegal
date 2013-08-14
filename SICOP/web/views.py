# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from web.models import Tbcaixa, Tbtipocaixa
from web.forms import FormPecasTecnicas
from django.http import request


@login_required
def acesso_restrito(request):    
    #form = FormPecasTecnicas()
    #return render_to_response("consultas.html",{"form":form}, context_instance = RequestContext(request))
    
    if request.method == "POST":
        retorno = request.POST['query']
    else:
        retorno = ''
        
    lista = Tbtipocaixa.objects.filter( nmtipocaixa__contains=retorno ).order_by('id')
    
    return render_to_response('sicop/acesso_restrito.html',{'lista':lista,'retorno':retorno}, 
                              context_instance = RequestContext(request))    
    
    