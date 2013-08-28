# Create your views here.
from django.template import loader
from django.http.response import HttpResponse
from django.template.context import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from reportlab.pdfgen import canvas
from django.utils.datetime_safe import date
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Image
import time
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from web.relatorio import relatorio_base
from web.models import Tbpecastecnicas


def relatorio(request):
    lista = Tbpecastecnicas.objects.all()
    return relatorio_base(request, lista)


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