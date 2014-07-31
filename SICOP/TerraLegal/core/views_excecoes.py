# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
import sys
from django import http
import traceback

def pagina_nao_encontrada(request):
    return render(request, "excecao/pagina_nao_encontrada.html")

def permissao_negada(request):
    return render(request, "excecao/permissao_negada.html")

def erro_servidor(request):
    
    #t = loader.get_template(template_name) # You need to create a 500.html template.
    ltype,lvalue,ltraceback = sys.exc_info()
    sys.exc_clear() #for fun, and to point out I only -think- this hasn't happened at 
                    #this point in the process already

    return render_to_response('/excecao/erro_servidor.html' ,{'type':lvalue}, context_instance = RequestContext(request))

 #   return http.HttpResponseServerError(t.render(Context({'type':ltype,'value':lvalue,'traceback':ltraceback})))
    
