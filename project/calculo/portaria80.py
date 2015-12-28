from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.forms import FormMunicipio
from project.tramitacao.models import Tbmunicipio, Tbsubarea, AuthUser, Tbdivisao, Tbuf
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from project.tramitacao.admin import verificar_permissao_grupo
from project.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

import webodt

from webodt.shortcuts import render_to
from webodt import shortcuts
from project import settings
from decimal import *
import os

import time
    
import xml
import csv
import unicodedata

nome_relatorio      = "relatorio_portaria80"
response_consulta  = "/sicop/restrito/portaria80/calculo/"
titulo_relatorio    = "Calculo Portaria 80 - Clausulas Resolutivas"


@permission_required('sicop.calculo_portaria80', login_url='/excecoes/permissao_negada/', raise_exception=True)
def calculo(request):
    
    filename = settings.CSV_PATH_DIR + '/fdis.csv'
    fdis = csv.DictReader(open(filename,"rb"),delimiter=',')
    l_fdis = []
    for line in fdis:
        l_fdis.append(line)
        
    
    filename = settings.CSV_PATH_DIR +'/fcon.csv'
    fcon = csv.DictReader(open(filename,"rb"),delimiter=',')
    l_fcon = []
    for line in fcon:
        l_fcon.append(line)
        
    #fanc indica o fator de ancianidade
    filename = settings.CSV_PATH_DIR +'/fanc.csv'
    fanc = csv.DictReader(open(filename,"rb"),delimiter=',')
    l_fanc = []
    for row in fanc:
        l_fanc.append(row)
    
    #fdim soh tem uma linha
    filename = settings.CSV_PATH_DIR +'/fdim.csv'
    fdim = csv.DictReader(open(filename,"rb"),delimiter=',')
    request.session[nome_relatorio] = []
    if request.method == "POST":
        if validacao(request):
            #busca dados do municipio no bd
            municipio  = Tbmunicipio.objects.get( pk = request.POST['municipio'])
            vlterranua = Decimal(municipio.vlterranua)
            nrmodulo = Decimal(municipio.nrmodulofiscal)
            nmmunicipio = municipio.nome_mun
            #dados que vem do pagina
            nrarea = Decimal((request.POST['nrarea']).replace(',','.')).quantize(Decimal('1.0000'))
            nrparcelas = Decimal(request.POST['nrparcelas'])
            nrparcelaspagas = Decimal(request.POST['nrparcelaspagas'])
            pfcon = Decimal(request.POST['fcon'])
            pfdis = Decimal(request.POST['fdis'])
            pfanc = request.POST['fanc']
            
            
            #print 'pfdis:' + str(pfdis) + ' pfcon:' + str(pfcon) +  ' pfanc:' + str(pfanc) 
            
            #inicio dos calculos
            nrmodulosarea = (nrarea/nrmodulo).quantize(Decimal('1.000000'))
            #print 'nrmodulosarea: ' + str(nrmodulosarea)
            
            #area a ser paga
            areaapagar = ((nrarea/nrparcelas) * (nrparcelas - nrparcelaspagas))#.quantize(Decimal('1.0000'))
            #print 'areaapagar:' + str(areaapagar)
            
            #dimensao do imovel fdim/dimensao
            for row in fdim:
                #values = row.values() print values print row['x'] print row['n']
                dimensao = (Decimal(row['x']) * nrmodulosarea + Decimal(row['n']))#.quantize(Decimal('1.0000000000'))
            #    print 'x:' + str(row['x']) +' ' +' n:'+ str(row['n']) + ' dimensao:' + str(dimensao)
           
            #calculo ancianidade
            #print len(l_fanc)
            if pfanc !='2':
                anosocupa = 1
            else:
                anosocupa = Decimal(request.POST['anosocupa'])
            dic = {}
            dic = l_fanc
            for row in dic:
                if pfanc == row['id']:
                    ancianidade = Decimal(str(row['y'])) * anosocupa + Decimal(str(row['x']))
            #        print 'acianidade:' + str(ancianidade)
            
            #calculo do valor da terra nua por hectare
            vlterranuaporha = (vlterranua * pfdis * pfcon * dimensao * ancianidade)#.quantize(Decimal('1.00'))
            #print 'total:' + str(vlterranuaporha)
            #calculo do valor do imovel
            vlimovel = (vlterranuaporha * areaapagar).quantize(Decimal('1.00'))
            vlterranuaporha = vlterranuaporha.quantize(Decimal('1.00'))
            
            lista = Tbmunicipio.objects.all().filter(codigo_uf__id__in=request.session['uf'])
            lista = lista.order_by( 'nome_mun' )
            anosocupa = request.POST['anosocupa']
            fdis = request.POST['fdis']
            fcon = request.POST['fcon']
            fanc = request.POST['fanc']
            nrarea = request.POST['nrarea']
            areaapagar = areaapagar.quantize(Decimal('1.0000'))
            
            dicionarios = {'lista':lista,'nrarea':nrarea,'nrparcelas':nrparcelas,
                           'nrparcelaspagas':nrparcelaspagas,
                           'municipio':municipio,'vlterranua':vlterranua,'nrmodulo':nrmodulo,
                           'l_fdis':l_fdis,'l_fcon':l_fcon,'l_fanc':l_fanc,
                           'anosocupa':anosocupa,
                           'fdis':fdis,'fcon':fcon,'fanc':fanc,
                           'nrmodulosarea':nrmodulosarea,
                           'vlterranuaporha':vlterranuaporha,'vlimovel':vlimovel,
                           'areaapagar':areaapagar
             
                            }
            
            request.session[nome_relatorio] = dicionarios
            return render_to_response('calculos/portaria80/calculo.html' ,dicionarios, context_instance = RequestContext(request))
        
            
            
    lista = Tbmunicipio.objects.all().filter(codigo_uf__id__in=request.session['uf'])
    lista = lista.order_by( 'nome_mun' )
    dicionarios = {'l_fdis':l_fdis,'l_fcon':l_fcon,'l_fanc':l_fanc,'lista':lista}
    
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_municipio'] = lista
    return render_to_response('calculos/portaria80/calculo.html' ,dicionarios, context_instance = RequestContext(request))


@permission_required('sicop.calculo_portaria80', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    auth_user = AuthUser.objects.get( pk = request.user.id )
    
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append(('Data do calculo: '+str(time.strftime("%d/%m/%Y"))+' Usuario: '+str(auth_user.username),''))
        dados.append(('Descricao','Valor'))
        dados.append(('Valor do imovel', 'R$ '+str(lista['vlimovel'])))
        dados.append(('Area do imovel',str(lista['nrarea'])+ ' hectares'))
        dados.append(('Total de parcelas',lista['nrparcelas']))
        dados.append(('Anos de ocupacao',str(lista['anosocupa'])+' anos'))
        dados.append(('Valor da terra nua','R$ '+str(lista['vlterranua'])))
        dados.append(('Modulos fiscais do municipio',lista['nrmodulo']))
        dados.append(('Modulos fiscais da area',lista['nrmodulosarea']))
        dados.append(('Valor da terra nua por hectare','R$ '+str(lista['vlterranuaporha'])))
        dados.append(('Area a pagar',str(lista['areaapagar'])+' hectares'))
       
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.gleba_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([ obj.nmgleba.encode('iso-8859-1').strip() , obj.tbsubarea.nmsubarea])
        return response
    else:
        return HttpResponseRedirect( response_consulta )

def validacao(request_form):
    warning = True
    if request_form.POST['anosocupa'] == '' and request_form.POST['fanc'] == '2' :
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade de anos de ocupacao')
        warning = False
    if request_form.POST['nrparcelas'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade de parcelas')
        warning = False
    if request_form.POST['nrparcelaspagas'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade de parcelas ja pagas')
        warning = False
        
    return warning
