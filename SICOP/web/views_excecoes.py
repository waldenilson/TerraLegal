# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

def pagina_nao_encontrada(request):
    return render(request, "excecoes/pagina_nao_encontrada.html")

def permissao_negada(request):
    return render(request, "excecoes/permissao_negada.html")

def erro_servidor(request):
    return render(request, "excecoes/erro_servidor.html")
