# Create your views here.
from django.template.context import Context
from django.template import loader
from django.http.response import HttpResponse

def home(request):
    template = loader.get_template("base.html")
    c = Context ({})
    return HttpResponse(template.render(c))