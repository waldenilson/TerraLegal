# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

def inicio(request):
    return render(request, "web/index.html")

def terra_legal(request):
    return render(request, "web/terra_legal.html")

def mda(request):
    return render(request, "web/mda.html")

def processo_rural(request):
    return render_to_response('web/processo_rural.html',{},
                              context_instance = RequestContext(request))
def regularizacao_urbana(request):
    return render_to_response('web/regularizacao_urbana.html',{},
                              context_instance = RequestContext(request))