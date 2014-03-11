
# -*- coding: UTF-8 -*-

from django.template.context import Context
from sicop.models import Tbprocessobase, Tbpecastecnicas, \
    Tbprocessorural, AuthUser
from sicop.relatorio_base import relatorio_base
from django.contrib.auth.decorators import permission_required
import webodt
from webodt.shortcuts import render_to_response, render_to
from fileinput import filename
import os
from django.http.response import HttpResponse, HttpResponseRedirect
import shutil
from TerraLegal import settings
from django.utils.datetime_safe import datetime


#PROCESSOS QUE TEM PECA TECNICA
@permission_required('sicop.processo_peca_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_peca(request):
        
    #buscar os processos que tem o cpf do requerente ligado a uma peca tecnica
    p_rural = Tbprocessorural.objects.filter( tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    p_rural_com_peca = []
    for r in p_rural:
        if Tbpecastecnicas.objects.filter( nrcpfrequerente = r.nrcpfrequerente.replace('.','').replace('-','') ):
            p_rural_com_peca.append( r )
    
    context = dict(         
                        titulo='Relatorio Processos com Peca Tecnica',
                        total=len(p_rural_com_peca),
                        lista=p_rural_com_peca
                  )
    
    return render_to_response('relatorio/processos-com-peca.odt',dictionary=context,format='odt',filename='relatorio-processos-com-peca.odt')

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
#    pecas = Tbpecastecnicas.objects.all()
    for g in glebas:
        print 'Gleba: '+str(g.nmgleba)
        qtd = 0
        for p in pecas:
            if p.tbgleba.id == g.id:
                qtd += 1
        print 'Total: '+str(qtd)

    context = dict(         
                        titulo='Relatório das Peças Técnicas por Gleba',
                        total=len(glebas),
                        glebas=glebas
                  )   

    return render_to_response('relatorio/pecas-por-gleba.odt',dictionary=context,format='odt',filename='relatorio-pecas-por-gleba.odt')

#PECAS TECNICAS NAO APROVADAS

@permission_required('sicop.peca_nao_aprovada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_nao_aprovada(request):
    
    #buscar as pecas tecnicas com status false
    pecas = Tbpecastecnicas.objects.filter( stpecatecnica = False )
    
    context = dict(         
                            titulo= 'Relatório das Peças Técnicas não Aprovadas',
                            total=len(pecas),
                            lista=pecas
                        )
    
    # requerente, caixa, gleba, area, perimetro, contrato, entrega, dsobservacao
    
    return render_to_response('relatorio/pecas-nao-aprovadas.odt',
                              dictionary=context,format='odt',
                              filename='relatorio-pecas-nao-aprovadas.odt')
    
#PECAS TECNICAS REJEITADAS

@permission_required('sicop.peca_rejeitada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_rejeitada(request):
    
    #buscar as pecas tecnicas nao enviadas pra brasilia
    pecas = Tbpecastecnicas.objects.filter( stenviadobrasilia = False )
    
    context = dict(        
                            titulo='Relatório das Peças Técnicas rejeitadas',
                            total=len(pecas),
                            lista=pecas
                        )
    
    return render_to_response('relatorio/pecas-rejeitadas.odt',dictionary=context,format='odt',filename='relatorio-pecas-rejeitadas.odt')
    
#PECAS TECNICAS SEM PROCESSO

@permission_required('sicop.peca_sem_processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_sem_processo(request):

    #buscar as pecas tecnicas que nao estao ligadas a um processo
    pecas = Tbpecastecnicas.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    pecas_sem_proc = []
    
    for p in pecas:
        if not Tbprocessorural.objects.filter( nrcpfrequerente = p.nrcpfrequerente ):
            pecas_sem_proc.append(p)
    
    context = dict(        
                    titulo='Relatório das Peças Técnicas sem processo',
                    total=len(pecas_sem_proc),
                    lista=pecas_sem_proc
                )
    
    return render_to_response('relatorio/pecas-sem-processo.odt',dictionary=context,format='odt',filename='relatorio-pecas-sem-processo.odt')

#PECAS TECNICAS VALIDADAS

@permission_required('sicop.peca_validada_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def peca_validada(request):
    
    #buscar as pecas tecnicas enviadas pra brasilia
    pecas = Tbpecastecnicas.objects.filter( stenviadobrasilia = True )
    print 'pecas validadas: '+str(pecas.count())
        
    context = dict(         
                    titulo='Relatório das Peças Técnicas validadas',
                    total=len(pecas),
                    lista=pecas
                )
    
    return render_to_response('relatorio/pecas-validadas.odt',dictionary=context,format='odt',filename='relatorio-pecas-validadas.odt')
    
