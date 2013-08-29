from django.http.response import HttpResponse
from reportlab.platypus.doctemplate import SimpleDocTemplate
import time
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from django.utils.datetime_safe import date
from reportlab.pdfgen import canvas
import Canvas
from reportlab.lib import styles
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def processo_peca(request):
    return render_to_response('sicop/restrito/relatorio/processo_peca.html',{},
                              context_instance = RequestContext(request))

def peca_gleba(request):
    return render_to_response('sicop/restrito/relatorio/peca_gleba.html',{},
                              context_instance = RequestContext(request))

def peca_nao_aprovada(request):
    return render_to_response('sicop/restrito/relatorio/peca_nao_aprovada.html',{},
                              context_instance = RequestContext(request))

def peca_rejeitada(request):
    return render_to_response('sicop/restrito/relatorio/peca_rejeitada.html',{},
                              context_instance = RequestContext(request))

def peca_sem_processo(request):
    return render_to_response('sicop/restrito/relatorio/peca_sem_processo.html',{},
                              context_instance = RequestContext(request))

def peca_validada(request):
    return render_to_response('sicop/restrito/relatorio/peca_validada.html',{},
                              context_instance = RequestContext(request))

