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
from sicop.models import Tbprocessobase, Tbpecastecnicas, Tbgleba,\
    Tbprocessorural
from sicop.relatorio_base import relatorio_base
from django.contrib.auth.decorators import permission_required

#PROCESSOS QUE TEM PECA TECNICA
@permission_required('sicop.processo_peca_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_peca(request):
    
    #buscar os processos que tem o cpf do requerente ligado a uma peca tecnica
    p_rural = Tbprocessorural.objects.all()
    p_rural_com_peca = []
    for r in p_rural:
        if Tbpecastecnicas.objects.all().filter( nrcpfrequerente = r.nrcpfrequerente.replace('.','').replace('-','') ):
            p_rural_com_peca.append( r )
    print 'total processos com peca: '+str(len(p_rural_com_peca))
    
    
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Processo x Peca')
    return resp

#PECAS TECNICAS POR GLEBAS
@permission_required('sicop.peca_gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_gleba(request):
    
    #buscar as pecas agrupadas por glebas
    pecas = Tbpecastecnicas.objects.distinct('tbgleba')
    glebas = []
    #buscando as glebas que tem pecas
    for obj in pecas:
        glebas.append( obj.tbgleba )
    
    #todas as pecas
    pecas = Tbpecastecnicas.objects.all()
    for g in glebas:
        print 'Gleba: '+str(g.nmgleba)
        qtd = 0
        for p in pecas:
            if p.tbgleba.id == g.id:
                qtd += 1
        print 'Total: '+str(qtd)
    
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Peca x Gleba')
    return resp

#PECAS TECNICAS NAO APROVADAS
@permission_required('sicop.peca_nao_aprovada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_nao_aprovada(request):
    
    #buscar as pecas tecnicas com status false
    pecas = Tbpecastecnicas.objects.filter( stpecatecnica = False )
    print 'pecas nao aprovadas: '+str(pecas.count())
    
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas nao Aprovadas')
    return resp

#PECAS TECNICAS REJEITADAS
@permission_required('sicop.peca_rejeitada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_rejeitada(request):
    
    #buscar as pecas tecnicas nao enviadas pra brasilia
    pecas = Tbpecastecnicas.objects.filter( stenviadobrasilia = False )
    print 'pecas rejeitadas: '+str(pecas.count())
    
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas Rejeitadas')
    return resp

#PECAS TECNICAS SEM PROCESSO
@permission_required('sicop.peca_sem_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_sem_processo(request):
    
    #buscar as pecas tecnicas que nao estao ligadas a um processo
    pecas = Tbpecastecnicas.objects.all()
    pecas_sem_proc = []
    for p in pecas:
        if not Tbprocessorural.objects.all().filter( nrcpfrequerente = p.nrcpfrequerente.replace('.','').replace('-','') ):
            pecas_sem_proc.append( p )
    print 'total pecas sem processo: '+str(len(pecas_sem_proc))


    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas sem Processos')
    return resp

#PECAS TECNICAS VALIDADAS
@permission_required('sicop.peca_validada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_validada(request):
    
    #buscar as pecas tecnicas enviadas pra brasilia
    pecas = Tbpecastecnicas.objects.filter( stenviadobrasilia = True )
    print 'pecas validadas: '+str(pecas.count())
        
    lista = Tbprocessobase.objects.all()
    resp = relatorio_base(request, lista, 'Pecas Validadas')
    return resp

