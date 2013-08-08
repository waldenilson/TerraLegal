# Create your views here.
from django.template.context import Context
from django.template import loader
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    template = loader.get_template("base.html")
    c = Context ({})
    return HttpResponse(template.render(c))

def search(request):
    return render_to_response()