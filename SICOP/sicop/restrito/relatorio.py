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
from sicop.models import Tbprocessobase
from sicop.relatorio_base import relatorio_base

def processo_peca(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Processo x Peca')
    return resp

def peca_gleba(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Peca x Gleba')
    return resp

def peca_nao_aprovada(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas nao Aprovadas')
    return resp

def peca_rejeitada(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas Rejeitadas')
    return resp

def peca_sem_processo(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas sem Processos')
    return resp

def peca_validada(request):
    # criar objeto lista resultante da consulta
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas Validadas')
    return resp

