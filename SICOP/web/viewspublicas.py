# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

def rural(request):
    retorno = ""
    return render_to_response('web/rural.html',{'retorno':retorno},
                              context_instance = RequestContext(request))
    

def urbano(request):
    
    js = "processos"
    return render_to_response('web/urbano.html',{'retorno':js},
                              context_instance = RequestContext(request))