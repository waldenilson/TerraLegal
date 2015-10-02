#coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from TerraLegal.tramitacao.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbloganalise, Tbcaixa, Tbgleba, Tbmunicipio, Tbuf,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia, Tbpregao,\
    Tbdivisao,   Tbetapa, Tbtransicao, Tbetapaposterior, Tbchecklistprocessobase,\
    Tbchecklist
from TerraLegal.livro.models import Tbtitulo, Tbstatustitulo, Tbtipotitulo , Tbtituloprocesso
from TerraLegal.geoinformacao.models import TbparcelaGeo
from TerraLegal.tramitacao.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from TerraLegal.tramitacao.restrito import processo_rural
from types import InstanceType
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
from TerraLegal.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header
from odslib import ODS
from django.contrib.auth.models import Permission
from TerraLegal.tramitacao import admin
from django.db.models import Q
from operator import  itemgetter, attrgetter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from calendar import monthrange
from datetime import timedelta
import csv
import sqlite3
import urllib2
from django.core import serializers
import json
from TerraLegal.livro.models import Tbtituloprocesso
from TerraLegal.documento.models import Sobreposicao

nome_relatorio      = "relatorio_processo"
response_consulta  = "/sicop/processo/consulta/"
titulo_relatorio    = "Relatorio Processos"
planilha_relatorio  = "Processos"

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consultaprocesso(request):

#    list_json()
#    batimento_cpf_processo("/opt/cpfs.csv","/opt/cpfs_.csv")
#    reader("/opt/cpfs.csv")
#    reader_ods("/opt/parcelas.ods")

#    export_to_sqlite_android('/opt/sicopsqlite.db')

#    tit = Tbtituloprocesso.objects.filter(id = 2616)
#    if tit[0].tbtitulo.tbcaixa is not None:
#        print 'ok'
#    refazer_movimentacao(request)

#    buscar_processos_sem_pecas_sicop_sigef(request,"/opt/cpf-sigef-abril.csv")
#    buscar_parcelas_sigef('44857225204')
#    sinc_parcelas()
#    parcela_kml()
# verificar batimento cpfs em mais de um processo sem estarem na tbprocessosanexos

    todos = []
    clausulas = Tbprocessoclausula.objects.all()
    rurais = Tbprocessorural.objects.all()

    total = 0
    for r in todos:
        cont = 0
        for r2 in todos:
            if r.nrcpfrequerente == r2.nrcpfrequerente:
                cont += 1
        if cont > 1:
            total += 1
            print r.nrcpfrequerente +' - '+str(cont)
    #print 'total '+str(total)

# verificar batimento cpfs em mais de um processo sem estarem na tbprocessosanexos

    numero =  request.POST['processo_base'].replace('.','').replace('/','').replace('-','')
    if not numero:

        #Tbmovimentacao.objects.filter( '' ).order_by( 'dtmovimentacao' )

        messages.add_message(request,messages.WARNING,'Processo nao preenchido corretamente')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

    if request.user.has_perm('sicop.processo_rural_consulta'):
            p_rural = Tbprocessorural.objects.filter( 
                Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])| 
                Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')
    if request.user.has_perm('sicop.processo_clausula_consulta'):
            p_clausula = Tbprocessoclausula.objects.filter( 
                Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])| # = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
                Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')
    if request.user.has_perm('sicop.processo_urbano_consulta'):
            p_urbano = Tbprocessourbano.objects.filter( 
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmpovoado') # = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = []
    for obj in p_rural:
       lista.append( obj )
    for obj in p_clausula:
        lista.append( obj )
    for obj in p_urbano:
        lista.append( obj )
    if not lista:
        messages.add_message(request,messages.WARNING,'Processo nao encontrado')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

    
    for obj in lista:
        request.session['processo_saida'] = 'unico'
        return HttpResponseRedirect("/sicop/processo/edicao/"+str(obj.tbprocessobase.id)+"/")
        #edicao(request,obj.tbprocessobase.id)
        #usar http_redirect alguma coisa assim passando a url do edicao  e o id

    return render_to_response('sicop/processo/rural/edicao.html',
                              context_instance = RequestContext(request))   

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    # carrega os processos da divisao do usuario logado
    lista = []
    #lista = Tbprocessobase.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by( "dtcadastrosistema" )
    if request.method == "POST":
        # consulta generica de processos
        numero = request.POST['numero'].replace('.','').replace('/','').replace('-','')
        
        # consulta de processo rural e clausula
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['requerente']
        
        # consulta de processo urbano
        cnpj = request.POST['cnpj']
        municipio = request.POST['municipio']
        p_rural = []
        p_clausula = []
        p_urbano = []
        #consulta titulo
        titulo = request.POST['cdtitulo']
        #as queries abaixo verificam dentre outras coisas, se o  processo que deseja consultar pertene a divisao do
        #usuario logado, neste caso , mesmo que nao esteja no escopo de sua divisao, o usuario logado pode 
        #acessar o processo.Mas o usuario logado nao pode tramitar este processo. Somente aquele que detem o 
        #processo tramitado para a sua divisao pode tramitar o processo.
        if len(numero) >= 3:
            if request.user.has_perm('sicop.processo_rural_consulta'):
                p_rural = Tbprocessorural.objects.filter( 
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])| #= AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')
            if request.user.has_perm('sicop.processo_clausula_consulta'):
                p_clausula = Tbprocessoclausula.objects.filter( 
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])| # = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')
            if request.user.has_perm('sicop.processo_urbano_consulta'):
                p_urbano = Tbprocessourbano.objects.filter( 
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(tbprocessobase__nrprocesso__contains = numero, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmpovoado') # = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            lista = []
            for obj in p_rural:
                lista.append( obj )
            for obj in p_clausula:
                lista.append( obj )
            for obj in p_urbano:
                lista.append( obj )
        else:
            if len(numero) > 0 and len(numero) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Processo.')
        
        if len(cpf) >= 3 :
            if request.user.has_perm('sicop.processo_rural_consulta'):
                p_rural = Tbprocessorural.objects.filter( 
                    Q(nrcpfrequerente__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nrcpfrequerente__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)|

                    Q(nrcpfconjuge__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nrcpfconjuge__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')#__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            if request.user.has_perm('sicop.processo_clausula_consulta'):
                p_clausula = Tbprocessoclausula.objects.filter( 
                    Q(nrcpfrequerente__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nrcpfrequerente__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)|# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
                    Q(nrcpfinteressado__contains = cpf, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            lista = []
            for obj in p_rural:
                lista.append( obj )
            for obj in p_clausula:
                lista.append( obj )
        else:
            if len(cpf) > 0 and len(cpf) < 3 :
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo CPF.')
                
        if len(requerente) >= 3 :
            if request.user.has_perm('sicop.processo_rural_consulta'):
                p_rural = Tbprocessorural.objects.filter( 
                    Q(nmrequerente__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nmrequerente__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)|# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )

                    Q(nmconjuge__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nmconjuge__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            if request.user.has_perm('sicop.processo_clausula_consulta'):
                p_clausula = Tbprocessoclausula.objects.filter( 
                    Q(nmrequerente__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nmrequerente__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)|# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
                    Q(nminteressado__icontains = requerente, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessoclausula',tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            lista = []
            for obj in p_rural:
                lista.append( obj )
            for obj in p_clausula:
                lista.append( obj )
        else:
            if len(requerente) > 0 and len(requerente) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Requerente.')
        
        if len(cnpj) >= 3 :
            if request.user.has_perm('sicop.processo_urbano_consulta'):
                p_urbano = Tbprocessourbano.objects.filter( 
                    Q(nrcnpj__contains = cnpj, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(nrcnpj__contains = cnpj, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano', tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmpovoado') # = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ) 
            lista = []
            for obj in p_urbano:
                lista.append( obj )
    
        if len(municipio) >= 3 :
            if request.user.has_perm('sicop.processo_urbano_consulta'):
                p_urbano = Tbprocessourbano.objects.filter( 
                    Q(tbprocessobase__tbmunicipio__nome_mun__icontains = municipio, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                    Q(tbprocessobase__tbmunicipio__nome_mun__icontains = municipio, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessourbano', tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmpovoado')# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ) 
            lista = []
            for obj in p_urbano:
                lista.append( obj ) 
        else:
            if len(municipio) > 0 and len(municipio) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Municipio.')
       
        if len(titulo) >= 3:
            if request.user.has_perm('sicop.livro_consulta'):
                p_titulo = Tbprocessorural.objects.all().filter(
                         Q(tbprocessobase__tbtitulo__cdtitulo__icontains = titulo, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbdivisao__id__in=request.session['divisoes'])|
                         Q(tbprocessobase__tbtitulo__cdtitulo__icontains = titulo, tbprocessobase__tbtipoprocesso__tabela = 'tbprocessorural', tbprocessobase__tbcaixa__tbdivisao__id = AuthUser.objects.get(pk=request.user.id).tbdivisao.id)).order_by('nmrequerente')
            lista = []
            for obj in p_titulo:
                lista.append( obj )
        else:
            if len(titulo) > 0 and len(titulo) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Titulo.')
                
    #para exibir o espelho quando o resultado for apenas 1 registro
    request.session['processo_saida'] = ''
    for obj in lista:
        if len(lista) == 1:
            request.session['processo_saida'] = 'unico'
            edicao(request,obj.tbprocessobase.id)
     
    #para exibir o espelho quando o resultado for apenas 1 registro
    if len(lista) == 1: 
        if 'tramitacao_massa_ativado' in request.session and request.session['tramitacao_massa_ativado']:
                add_tramitacao_massa(request, lista[0].tbprocessobase.id)
        else:
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(lista[0].tbprocessobase.id))
    lista_processo_titulo = []
    if lista:
        for obj in lista:
            try:
                lista_processo_titulo.append (Tbtituloprocesso.objects.get(tbprocessobase__id = obj.tbprocessobase.id))
            except:
                pass
                             
    # gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_processo'] = lista
        
    return render_to_response('sicop/processo/consulta.html',{'lista':lista,'lista_processo_titulo':lista_processo_titulo}, context_instance = RequestContext(request))

@permission_required('sicop.processo_tramitar', login_url='/excecoes/permissao_negada/', raise_exception=True)
def tramitar(request, base):
    if request.method == "POST":
        
        base = get_object_or_404(Tbprocessobase, id=base )
        caixadestino = request.POST['tbcaixadestino']
        caixaorigem  = base.tbcaixa
        if validarTramitacao(request, base, caixaorigem, caixadestino):
            # atualizar processobase com caixa tramitada
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = base.nrprocesso,
                                    tbgleba = base.tbgleba,
                                    tbmunicipio = base.tbmunicipio,
                                    tbcaixa = Tbcaixa.objects.get( pk = caixadestino),
                                    tbtipoprocesso = base.tbtipoprocesso,
                                    tbetapaatual = base.tbetapaatual,
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    auth_user = base.auth_user,
                                    tbdivisao = base.tbdivisao,
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                    nmendereco = base.nmendereco,
                                    nmcontato = base.nmcontato,
                                    tbtitulo = base.tbtitulo,
                                    tbmunicipiodomicilio = base.tbmunicipiodomicilio
                                    )
            f_base.save()
            # criar registro da movimentacao
            f_movimentacao = Tbmovimentacao(
                                           tbprocessobase = base,
                                           tbcaixa_id = Tbcaixa.objects.get( pk = caixadestino).id,
                                           tbcaixa_id_origem = caixaorigem,
                                           auth_user = AuthUser.objects.get( pk = request.user.id ),
                                           dtmovimentacao = datetime.datetime.now()
                                           )
            f_movimentacao.save()
            
            #OBS ao tramitar o processo todos os processos anexados serao tramitados ( classificado como anexo )
            anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )
            for nx in anexado:
                proc_anexado = nx.tbprocessobase_id_anexo
                f_base = Tbprocessobase (
                                        id = proc_anexado.id,
                                        nrprocesso = proc_anexado.nrprocesso,
                                        tbgleba = proc_anexado.tbgleba,
                                        tbmunicipio = proc_anexado.tbmunicipio,
                                        tbcaixa = Tbcaixa.objects.get( pk = caixadestino),
                                        tbtipoprocesso = proc_anexado.tbtipoprocesso,
                                        tbetapaatual = proc_anexado.tbetapaatual,
                                        dtcadastrosistema = proc_anexado.dtcadastrosistema,
                                        auth_user = proc_anexado.auth_user,
                                        tbdivisao = proc_anexado.tbdivisao,
                                        tbclassificacaoprocesso = proc_anexado.tbclassificacaoprocesso,
                                        nmendereco = base.nmendereco,
                                        nmcontato = base.nmcontato
                                        )
                f_base.save()
                    
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
        #segue abaixo se a validacao da tramitacao nao der certo
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        tipo = base.tbtipoprocesso.tabela
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase__id = base.id ).order_by( "-dtmovimentacao" ) 
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )
        
        #pre-selecao das caixas exibidas como caixa destino. Verifica a classe da divisao
        caixasdestino = Tbcaixa.objects.all().filter(
                Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id)|
                Q(tbtipocaixa__nmtipocaixa__icontains='ENT')
                )        
        

        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase__id = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            # caixas que podem ser tramitadas
            tram = []
            for obj in caixasdestino:
                if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == 'ENT' :
                    tram.append( obj )
            return render_to_response('sicop/processo/rural/edicao.html',
                                      {'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase__id = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                # caixas que podem ser tramitadas
                tram = []
                for obj in Tbcaixa.objects.filter(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id):
                    if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB':
                        tram.append( obj )               
                return render_to_response('sicop/processo/urbano/edicao.html',
                                          {'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase__id = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    dtrequerimento = formatDataToText( clausula.dtrequerimento )
                    # caixas que podem ser tramitadas
                    tram = []
                    for obj in Tbcaixa.objects.filter(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id):
                        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB':
                            tram.append( obj )
                    return render_to_response('sicop/processo/clausula/edicao.html',
                                              {'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao, 'dtrequerimento':dtrequerimento}, context_instance = RequestContext(request))      

@permission_required('sicop.processo_criar_pendencia', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criar_pendencia(request, base):
    if request.method == "POST":
        
        base = get_object_or_404(Tbprocessobase, id=base )
        descricao = request.POST['dspendencia']
        status_pendencia = request.POST['tbstatuspendencia']     
        tipo_pendencia = request.POST['tbtipopendencia']
           
        if validarPendencia(request, base, descricao,status_pendencia,tipo_pendencia):
            
            f_pendencia = Tbpendencia(
                                      tbprocessobase = base,
                                      auth_user = AuthUser.objects.get( pk = request.user.id ),
                                      auth_user_updated = AuthUser.objects.get( pk = request.user.id ),
                                      tbtipopendencia  = Tbtipopendencia.objects.get( pk = request.POST['tbtipopendencia'] ),
                                      tbstatuspendencia = Tbstatuspendencia.objects.get( pk = request.POST['tbstatuspendencia'] ) ,
                                      dsdescricao = descricao,
                                      dtpendencia = datetime.datetime.now()
                                      )
            f_pendencia.save()
                    
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
        
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        tipo = base.tbtipoprocesso.tabela
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase__id = base.id ).order_by( "-dtmovimentacao" ) 
        # caixa destino
        caixadestino = Tbcaixa.objects.all()
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )


        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase__id = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/processo/rural/edicao.html',
                                      {'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase__id = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/processo/urbano/edicao.html',
                                          {'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase__id = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    dtrequerimento = formatDataToText( clausula.dtrequerimento )
                    return render_to_response('sicop/processo/clausula/edicao.html',
                                              {'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao,'dtrequerimento':dtrequerimento}, context_instance = RequestContext(request))      

@permission_required('sicop.processo_anexar', login_url='/excecoes/permissao_negada/', raise_exception=True)
def anexar(request, base):
        base = get_object_or_404(Tbprocessobase, id=base )
        processoanexo = request.POST['processoanexo'].replace('.','').replace('/','').replace('-','')
        if validarAnexo(request, base, processoanexo):
  
            #criar registro na tabela tbprocessosanexos
            proc_anexo = Tbprocessobase.objects.get( nrprocesso = processoanexo )
            f_anexos = Tbprocessosanexos(
                                         tbprocessobase = base,
                                         tbprocessobase_id_anexo = proc_anexo,
                                         auth_user = AuthUser.objects.get( pk = request.user.id ),
                                         dtanexado = datetime.datetime.now()
                                        )
            f_anexos.save()
            #atualizar a classificacao do processo_anexo para anexo 
            f_anexo = Tbprocessobase (
                                    id = proc_anexo.id,
                                    nrprocesso = proc_anexo.nrprocesso,
                                    tbgleba = proc_anexo.tbgleba,
                                    tbmunicipio = proc_anexo.tbmunicipio,
                                    tbcaixa = base.tbcaixa,
                                    tbtipoprocesso = proc_anexo.tbtipoprocesso,
                                    tbetapaatual = proc_anexo.tbetapaatual,
                                    dtcadastrosistema = proc_anexo.dtcadastrosistema,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = base.tbdivisao,
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 2 ),
                                    nmendereco = base.nmendereco,
                                    nmcontato = base.nmcontato,
                                    tbtitulo = base.tbtitulo,
                                    tbmunicipiodomicilio = base.tbmunicipiodomicilio
                                  
                                    )
            f_anexo.save()
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
        
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        tipo = base.tbtipoprocesso.tabela
        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase__id = base.id ).order_by( "-dtmovimentacao" ) 
        # caixa destino
        caixadestino = Tbcaixa.objects.all()
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )


        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase__id = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/processo/rural/edicao.html',
                                      {'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase__id = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/processo/urbano/edicao.html',
                                          {'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase__id = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    dtrequerimento = formatDataToText( clausula.dtrequerimento )
                    return render_to_response('sicop/processo/clausula/edicao.html',
                                              {'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao,'dtrequerimento':dtrequerimento}, context_instance = RequestContext(request))      

@permission_required('sicop.processo_desanexar', login_url='/excecoes/permissao_negada/', raise_exception=True)
def desanexar(request,id_anexo):
    id_processo_anexo =  get_object_or_404(Tbprocessosanexos, tbprocessobase_id_anexo=id_anexo)
    base =          get_object_or_404(Tbprocessobase, id = id_processo_anexo.tbprocessobase.id)
    proc_anexo =    get_object_or_404(Tbprocessobase, id = id_processo_anexo.tbprocessobase_id_anexo.id)
    if validarDesAnexo(request, base, proc_anexo):
        #remover o registro que anexa os processos entre si
        id_processo_anexo.delete()
        #atualizar a classificacao do processo_anexo para pai (desanexar)
        f_anexo = Tbprocessobase (
                                id = proc_anexo.id,
                                nrprocesso = proc_anexo.nrprocesso,
                                tbgleba = proc_anexo.tbgleba,
                                tbmunicipio = proc_anexo.tbmunicipio,
                                tbcaixa = base.tbcaixa,
                                tbtipoprocesso = proc_anexo.tbtipoprocesso,
                                tbetapaatual = proc_anexo.tbetapaatual,
                                dtcadastrosistema = proc_anexo.dtcadastrosistema,
                                auth_user = AuthUser.objects.get( pk = request.user.id ),
                                tbdivisao = base.tbdivisao,
                                tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                nmendereco = base.nmendereco,
                                nmcontato = base.nmcontato,
                                tbtitulo = base.tbtitulo,
                                tbmunicipiodomicilio = base.tbmunicipiodomicilio
                                )
        f_anexo.save()
        messages.add_message(request, messages.WARNING, 'Processo desanexado')
        return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
  
        #se nao passar na validacao
        
    carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
    carregarTbAuxFuncoesProcesso(request, base)

    tipo = base.tbtipoprocesso.tabela
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase__id = base.id ).order_by( "-dtmovimentacao" ) 
    # caixa destino
    caixadestino = Tbcaixa.objects.all()
    # anexos deste processo
    anexado = Tbprocessosanexos.objects.filter( tbprocessobase__id = base.id )


    if tipo == "tbprocessorural":
        rural = Tbprocessorural.objects.get( tbprocessobase__id = base.id )
        peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
        return render_to_response('sicop/processo/rural/edicao.html',
                                  {'gleba':gleba,
                                   'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                   'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                   'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
    else:
        if tipo == "tbprocessourbano":
            urbano = Tbprocessourbano.objects.get( tbprocessobase__id = base.id )
     
            dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
            dttitulacao = formatDataToText( urbano.dttitulacao )
            
            return render_to_response('sicop/processo/urbano/edicao.html',
                                      {'gleba':gleba,'situacaogeo':situacaogeo,
                                   'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                   'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                   'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                   'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessoclausula":
                clausula = Tbprocessoclausula.objects.get( tbprocessobase__id = base.id )
                dttitulacao = formatDataToText( clausula.dttitulacao )
                dtrequerimento = formatDataToText( clausula.dtrequerimento )
                return render_to_response('sicop/processo/clausula/edicao.html',
                                          {'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                   'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                   'base':base,'clausula':clausula,'dttitulacao':dttitulacao,'dtrequerimento':dtrequerimento}, context_instance = RequestContext(request))      

def def_fluxo( tp ):
    ordem = Tbetapa.objects.filter( tbtipoprocesso__id = tp, tbdivisao__id = 1, blativo = True ).values('ordem').annotate(dcount=Count('ordem')).order_by('ordem')
    fluxo = []
    for obj in ordem:
        etapa_ordem = Tbetapa.objects.filter( tbtipoprocesso__id = tp, tbdivisao__id = 1, ordem = obj.get('ordem'), blativo = True ).order_by('ordem','id')
        ordem = []
        for obj2 in etapa_ordem:
            ordem.append( obj2 )
        fluxo.append( ordem )
    return fluxo
    
@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):

    base = get_object_or_404(Tbprocessobase, id=id)
    carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
    carregarTbAuxFuncoesProcesso(request, base)
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    
    try :
        titulo_processo = Tbtituloprocesso.objects.get(tbprocessobase__id = base.id)
    except:
        titulo_processo = []

    
    # municipios da divisao do usuario logado E municipios associados a DIVISAO que criou o processo
    municipio = Tbmunicipio.objects.all().filter( 
        Q(codigo_uf__in=request.session['uf'])| 
        Q(codigo_uf= base.tbcaixa.tbdivisao.tbuf.id))# = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    
    tipo = base.tbtipoprocesso.tabela
    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" ) 
    # anexos deste processo
    anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )
    
    #se processobase pertencer a mesma divisao do usuario logado(teste anterior)
    #if base.auth_user.tbdivisao.id == AuthUser.objects.get( pk = request.user.id ).tbdivisao.id:
    #mudar para: se o processo estah numa CAIXA que pertenca a divisao do usuario logado OU estiver numa caixa de entrada OU
    # a classe do usuario eh maior que a classe da divisao a qual pertence o processo OU a divisao do usuario eh a divisao do processo
    
    #adiciona a lista de glebas, aquelas que estao associada a divisao do processo, pois o processo pode ser,
    #por exemplo da SRFA02 e esteja tramitado para a SRFA01.
    #efeito colateral a ser combatido: se o processo estiver na divisao do usuario , nao precisa adicionar estas glebas
    
    if base.tbcaixa.tbdivisao.id !=  AuthUser.objects.get( pk = request.user.id ).tbdivisao.id:
        for obj in Tbgleba.objects.all().filter(tbuf__id = base.tbcaixa.tbdivisao.tbuf.id):
            gleba.append(obj)
    
    if base.tbcaixa.tbdivisao.id == AuthUser.objects.get( pk = request.user.id ).tbdivisao.id or base.tbcaixa.tbtipocaixa.nmtipocaixa=="ENT" or AuthUser.objects.get( pk = request.user.id ).tbdivisao.nrclasse > base.tbdivisao.nrclasse or AuthUser.objects.get( pk = request.user.id ).tbdivisao.id == base.tbdivisao.id:
        #caixasdestino = Tbcaixa.objects.all().order_by("nmlocalarquivo")
        caixasdestino = Tbcaixa.objects.all().filter(
                Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id)|
                Q(tbtipocaixa__nmtipocaixa__icontains='ENT')
                ).order_by('nmlocalarquivo')

        etapas = []
        etapa_atual = None
        posteriores = {}
        
        # localizando processo principal apartir do anexo
        processo_principal = []        
        if base.tbclassificacaoprocesso.id == 2:
            obj = Tbprocessosanexos.objects.filter( tbprocessobase_id_anexo = id )[0]
            processo_principal = obj.tbprocessobase
     
        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            etapas = Tbetapa.objects.filter( tbtipoprocesso__id = rural.tbprocessobase.tbtipoprocesso.id, blativo = True ).order_by('ordem')
            transicao = Tbtransicao.objects.filter( tbprocessobase__id = rural.tbprocessobase.id ).order_by('-dttransicao')
            if transicao:
                etapa_atual = transicao[0]                
                posteriores = Tbetapaposterior.objects.filter( tbetapa__id = etapa_atual.tbetapa.id )
            #try:
            #    titulo = Tbtitulo.objects.get(tbprocessobase = id)
            #except ObjectDoesNotExist:
            #    titulo = []
            #if peca:
            #    peca = peca[0] 
            # caixas que podem ser tramitadas
            tram = []
            fluxo = def_fluxo(rural.tbprocessobase.tbtipoprocesso.id)
                        
            for obj in caixasdestino:
                if obj.blativo and ( obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == 'ENT' ) :
                    tram.append( obj )


            # buscar parcelas do sigef pelo webservice do sigef
            idkmls = []
            parcelas = []
            total_area_sigef = 0.0
            try:
                response = urllib2.urlopen('https://sigef.incra.gov.br/api/destinacao/parcelas/?cpf='+rural.nrcpfrequerente,timeout=1)
                retorno = json.loads(response.read())
                #jsonparcelas = serializers.serialize('json', html)
                #print 'pagina: '+str(retorno['parcelas'])
                x = 0
                for parcela in retorno['parcelas']:
                    x +=1
                    for mun in parcela['municipios']: 
                        parc = dict()
                        parc['parcela'] = 'Parcela '+str(x)
                        parc['imovel'] = parcela['nome']
                        parc['area'] = mun['area_parcela']
                        parc['nome'] = mun['nome'].encode("utf-8")+' / '+mun['uf'].encode("utf-8")
                        parcelas.append(parc)
                        total_area_sigef += mun['area_parcela']
                    idkmls.append(parcela['id'])
            except:
                pass

            #Dados da verificacao sobreposicao
            lista_sobreposicao = Sobreposicao.objects.filter( tbprocessobase__id = Tbprocessobase.objects.get(pk=rural.tbprocessobase.id).id )
            if lista_sobreposicao:
                documento_sobreposicao = lista_sobreposicao[0]
            else:
                documento_sobreposicao = Sobreposicao()


            #PARCELA(S)
            parcelas_geo = TbparcelaGeo.objects.filter( cpf_detent = rural.nrcpfrequerente )
            if parcelas_geo:
                nome_imovel = parcelas_geo[0].nome
                nome_gleba = parcelas_geo[0].gleba
                nome_municipio = Tbmunicipio.objects.filter( codigo_mun = parcelas_geo[0].municipio )[0].nome_mun
                area_imovel = 0.0
                for p in parcelas_geo:
                    area_imovel += float(p.area_ha_ut)
            else:
                nome_imovel = ''
                nome_gleba = ''
                nome_municipio = ''
                area_imovel = ''

            return render_to_response('sicop/processo/rural/edicao.html',
                                      {'nome_imovel':nome_imovel,'nome_gleba':nome_gleba,'n_parcelas':str(len(parcelas_geo)),
                                       'nome_municipio':nome_municipio,'area_imovel':area_imovel,'parcelas_geo':parcelas_geo,
                                       'sobreposicao':documento_sobreposicao,'total_area_sigef':total_area_sigef,'parcelas':parcelas,'kmls':idkmls,'transicao':transicao,'fluxo':fluxo,'gleba':gleba,'fases':etapas,'etapa_atual':etapa_atual,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,'processo_principal':processo_principal,
                                       'base':base,'rural':rural,'peca':peca,'statustitulo':statustitulo,'posteriores':posteriores,
                                       'municipiodomicilio':Tbmunicipio.objects.all(),'tipotitulo':tipotitulo,'titulo_processo':titulo_processo}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = id )
                pregao = Tbpregao.objects.all().order_by('nrpregao')
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                fases = Tbetapa.objects.filter( tbtipoprocesso__id = urbano.tbprocessobase.tbtipoprocesso.id, blativo = True ).order_by('ordem')
                transicao = Tbtransicao.objects.filter( tbprocessobase__id = urbano.tbprocessobase.id ).order_by('-dttransicao')
                if transicao:
                    etapa_atual = transicao[0]                
                    posteriores = Tbetapaposterior.objects.filter( tbetapa__id = etapa_atual.tbetapa.id )
                # caixas que podem ser tramitadas
                tram = []
                fluxo = def_fluxo( urbano.tbprocessobase.tbtipoprocesso.id )
                for obj in caixasdestino:
                    if obj.blativo and ( obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == 'ENT' ) :
                        tram.append( obj )
                return render_to_response('sicop/processo/urbano/edicao.html',
                                          {'transicao':transicao,'fluxo':fluxo,'gleba':gleba,'situacaogeo':situacaogeo,'etapa_atual':etapa_atual,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,'fases':fases,'pregao':pregao,'posteriores':posteriores,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,'processo_principal':processo_principal,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = id )
                    #dttitulacao = formatDataToText( clausula.dttitulacao )
                    #dtrequerimento = formatDataToText( clausula.dtrequerimento )
                    fases = Tbetapa.objects.filter( tbtipoprocesso__id = clausula.tbprocessobase.tbtipoprocesso.id, blativo = True ).order_by('ordem')
                    transicao = Tbtransicao.objects.filter( tbprocessobase__id = clausula.tbprocessobase.id ).order_by('-dttransicao')
                    if transicao:
                        etapa_atual = transicao[0]                
                        posteriores = Tbetapaposterior.objects.filter( tbetapa__id = etapa_atual.tbetapa.id )
                    # caixas que podem ser tramitadas
                
                    tram = []
                    fluxo = def_fluxo( clausula.tbprocessobase.tbtipoprocesso.id )
                    for obj in caixasdestino:
                        if obj.blativo and ( obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'RES' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == 'ENT' ) :
                            tram.append( obj )
                    
                    prazos = prazo_notificacao_clausula( clausula )

                    return render_to_response('sicop/processo/clausula/edicao.html',
                                              {'transicao':transicao,'prazos':prazos,'fluxo':fluxo,'gleba':gleba,'fases':fases,'etapa_atual':etapa_atual,'posteriores':posteriores,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,'processo_principal':processo_principal,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'analises':Tbloganalise.objects.filter( tbprocessobase__id = base.id ).order_by('dtanalise')}, context_instance = RequestContext(request))
        
    return HttpResponseRedirect("/sicop/processo/consulta/")
    
@permission_required('sicop.processo_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    escolha = "tbprocessorural"
    div_processo = "rural"
        
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
           
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            div_processo = "rural"
            carregarTbAuxProcesso(request, 'PAD')
            etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 1 ).order_by('ordem')
            return render_to_response('sicop/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'etapaprocesso':etapaprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'municipiodomicilio':Tbmunicipio.objects.all(),'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
        else:
            if escolha == "tbprocessourbano":
                div_processo = "urbano"
                carregarTbAuxProcesso(request, 'URB')
                etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 3 ).order_by('ordem')
                pregao = Tbpregao.objects.all().order_by('nrpregao')
                return render_to_response('sicop/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'etapaprocesso':etapaprocesso,'gleba':gleba,
                     'caixa':caixa,'municipio':municipio,'processo':escolha,'pregao':pregao,
                    'div_processo':div_processo,'contrato':contrato,'situacaogeo':situacaogeo},
                    context_instance = RequestContext(request));  
            else:
                if escolha == "tbprocessoclausula":
                    div_processo = "clausula"
                    form = FormProcessoClausula()
                    carregarTbAuxProcesso(request, 'RES')
                    etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 2 ).order_by('ordem')
                    return render_to_response('sicop/processo/cadastro.html',
                    {'form':form,'tipoprocesso':tipoprocesso,'etapaprocesso':etapaprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
    carregarTbAuxProcesso(request, 'PAD')   
    etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 1 ).order_by('ordem')
    return render_to_response('sicop/processo/cadastro.html',{'gleba':gleba,'caixa':caixa,'municipio':municipio,'municipiodomicilio':Tbmunicipio.objects.all(),
            'tipoprocesso':tipoprocesso,'processo':escolha,'div_processo':div_processo,'etapaprocesso':etapaprocesso}, context_instance = RequestContext(request))



#metodos da tramitacao em lote

@permission_required('sicop.processo_tramitacao_massa', login_url='/excecoes/permissao_negada/', raise_exception=True)
def ativar_tramitacao_massa(request):
    
    if 'tramitacao_massa_ativado' not in request.session:
        request.session['tramitacao_massa_ativado'] = True
        request.session['tramitacao_massa'] = []
    else:
        if request.session['tramitacao_massa_ativado']:
            request.session['tramitacao_massa_ativado'] = False
        else:
            request.session['tramitacao_massa_ativado'] = True
            request.session['tramitacao_massa'] = []
     
    return HttpResponseRedirect("/sicop/processo/consulta/")

@permission_required('sicop.processo_tramitacao_massa', login_url='/excecoes/permissao_negada/', raise_exception=True)
def add_tramitacao_massa(request, base):

    obj = get_object_or_404(Tbprocessobase,id=base)
    processo = None
    if obj.tbtipoprocesso.tabela == 'tbprocessorural':
        processo = get_object_or_404(Tbprocessorural,tbprocessobase__id=base)                
    elif obj.tbtipoprocesso.tabela == 'tbprocessoclausula':
        processo = get_object_or_404(Tbprocessoclausula,tbprocessobase__id=base)
    if obj.tbtipoprocesso.tabela == 'tbprocessourbano':
        processo = get_object_or_404(Tbprocessourbano,tbprocessobase__id=base)
    
    if not request.session['tramitacao_massa']:
        lista = []
        if processo.tbprocessobase.tbclassificacaoprocesso.id == 1:
            lista.append( processo )
        request.session['tramitacao_massa'] = lista
    else:
        lista = request.session['tramitacao_massa']
        achou = False
        
        for o in lista:
            if o.tbprocessobase.id == processo.tbprocessobase.id:
                achou = True
                break 
        
        if not achou:
            if processo.tbprocessobase.tbclassificacaoprocesso.id == 1:
                lista.append( processo )
            request.session['tramitacao_massa'] = lista
        
    return HttpResponseRedirect("/sicop/processo/consulta/")

@permission_required('sicop.processo_tramitacao_massa', login_url='/excecoes/permissao_negada/', raise_exception=True)
def rem_tramitacao_massa(request, base):

    obj = get_object_or_404(Tbprocessobase,id=base)
    processo = None
    if obj.tbtipoprocesso.tabela == 'tbprocessorural':
        processo = get_object_or_404(Tbprocessorural,tbprocessobase__id=base)                
    elif obj.tbtipoprocesso.tabela == 'tbprocessoclausula':
        processo = get_object_or_404(Tbprocessoclausula,tbprocessobase__id=base)
    if obj.tbtipoprocesso.tabela == 'tbprocessourbano':
        processo = get_object_or_404(Tbprocessourbano,tbprocessobase__id=base)
    
    
    lista = request.session['tramitacao_massa']
    lista.remove( processo )
    request.session['tramitacao_massa'] = lista
        
    return HttpResponseRedirect("/sicop/processo/lista_tramitacao_massa/")

@permission_required('sicop.processo_tramitacao_massa', login_url='/excecoes/permissao_negada/', raise_exception=True)
def executar_tramitacao_massa(request):
    
    lista = request.session['tramitacao_massa']

    if request.method != "POST":
        pass
    else:
        for obj in lista:
            base = obj.tbprocessobase
            
            caixadestino = request.POST['tbcaixadestino']
            caixaorigem  = base.tbcaixa
            if validarTramitacao(request, base, caixaorigem, caixadestino):
                # atualizar processobase com caixa tramitada
                f_base = Tbprocessobase (
                                        id = base.id,
                                        nrprocesso = base.nrprocesso,
                                        tbgleba = base.tbgleba,
                                        tbmunicipio = base.tbmunicipio,
                                        tbcaixa = Tbcaixa.objects.get( pk = caixadestino),
                                        tbtipoprocesso = base.tbtipoprocesso,
                                        tbetapaatual = base.tbetapaatual,
                                        dtcadastrosistema = base.dtcadastrosistema,
                                        auth_user = base.auth_user,
                                        tbdivisao = base.tbdivisao,
                                        tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                        nmendereco = base.nmendereco,
                                        nmcontato = base.nmcontato,
                                        tbtitulo = base.tbtitulo,
                                        tbmunicipiodomicilio = base.tbmunicipiodomicilio
                                        )
                f_base.save()
                # criar registro da movimentacao
                f_movimentacao = Tbmovimentacao(
                                               tbprocessobase = base,
                                               tbcaixa_id = Tbcaixa.objects.get( pk = caixadestino).id,
                                               tbcaixa_id_origem = caixaorigem,
                                               auth_user = AuthUser.objects.get( pk = request.user.id ),
                                               dtmovimentacao = datetime.datetime.now()
                                               )
                f_movimentacao.save()
                
                #OBS ao tramitar o processo todos os processos anexados serao tramitados ( classificado como anexo )
                anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id )
                for nx in anexado:
                    proc_anexado = nx.tbprocessobase_id_anexo
                    f_base = Tbprocessobase (
                                            id = proc_anexado.id,
                                            nrprocesso = proc_anexado.nrprocesso,
                                            tbgleba = proc_anexado.tbgleba,
                                            tbmunicipio = proc_anexado.tbmunicipio,
                                            tbcaixa = Tbcaixa.objects.get( pk = caixadestino),
                                            tbtipoprocesso = proc_anexado.tbtipoprocesso,
                                            tbetapaatual = proc_anexado.tbetapaatual,
                                            dtcadastrosistema = proc_anexado.dtcadastrosistema,
                                            auth_user = proc_anexado.auth_user,
                                            tbdivisao = proc_anexado.tbdivisao,
                                            tbclassificacaoprocesso = proc_anexado.tbclassificacaoprocesso,
                                            nmendereco = base.nmendereco,
                                            nmcontato = base.nmcontato,
                                            tbmunicipiodomicilio = base.tbmunicipiodomicilio
                                            )
                    f_base.save()
        return ativar_tramitacao_massa(request)

    return render_to_response('sicop/processo/lista_tramitacao_massa.html',{'caixadestino':Tbcaixa.objects.filter( blativo = True,tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id).order_by('nmlocalarquivo'),'lista':lista}, context_instance = RequestContext(request))



# metodos relatorios

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NUMERO','TIPO') )
        for obj in lista:
            dados.append( ( obj.tbprocessobase.nrprocesso , obj.tbprocessobase.tbtipoprocesso.nome ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(lista), ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Numero' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbprocessobase.tbtipoprocesso.nome)    
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Numero', 'Tipo'])
        for obj in lista:
            writer.writerow([obj.tbprocessobase.nrprocesso, obj.tbprocessobase.tbtipoprocesso.nome])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



# metodos classe controle

def validarTramitacao(request_form, base, origem, destino):
    warning = True
    if  base.tbclassificacaoprocesso.id == 2:
        messages.add_message(request_form,messages.WARNING,'Processo Anexo nao pode ser tramitado.')
        warning = False
    if origem.id == Tbcaixa.objects.get( pk = destino).id:
        messages.add_message(request_form,messages.WARNING,'Processo ja encontra-se no local de destino.')
        warning = False    
    if origem.tbtipocaixa.nmtipocaixa != "ENT" and origem.tbdivisao != AuthUser.objects.get(pk= request_form.user.id ).tbdivisao:
        messages.add_message(request_form,messages.WARNING,'Processo esta em divisao que nao pode ser tramitada pelo seu usuario.')
        warning = False  
    
    return warning
   
def validarPendencia(request_form, base, descricao,status_pendencia,tipo_pendencia):
    warning = True
    if descricao == '':
        messages.add_message(request_form, messages.WARNING, 'Informe a descricao da pendencia.')
        warning = False
    #verificar se o processo esta no dominio de outra divisao. Caso positivo, nao pode alterar/inserir pendencia
    if base.tbdivisao != Tbdivisao.objects.get(pk=AuthUser.objects.get( pk=request_form.user.id  ).tbdivisao.id ):
        messages.add_message(request_form, messages.WARNING, 'O processo esta tramitado para outra divisao/sede. Nao pode ser editado')
        warning = False   
        
    if status_pendencia == '':
        messages.add_message(request_form, messages.WARNING, 'Informe o status da pendencia.')
        warning = False
        
    if tipo_pendencia == '':
        messages.add_message(request_form, messages.WARNING, 'Informe o tipo da pendencia.')
        warning = False
        
    return warning

def validarAnexo(request_form, base, processoanexo):
    global fgexiste 
    warning = True
    #verificar se campo processo a anexar esta em branco
    if processoanexo == '':
        messages.add_message(request_form, messages.WARNING, 'Informe o numero do processo a anexar.')
        warning = False
    #verificar se processo a anexar eh o mesmo processo base
    if processoanexo == base.nrprocesso:
        messages.add_message(request_form, messages.WARNING, 'Nao permitido anexar o proprio processo.')
        warning = False
    #verificar se processo a anexar existe e pertence a divisao do usuario
    proc_anexo = Tbprocessobase.objects.all().filter( nrprocesso = processoanexo)#, auth_user__tbdivisao = AuthUser.objects.get( pk = request_form.user.id ).tbdivisao )
    if not proc_anexo:
        messages.add_message(request_form, messages.WARNING, 'O processo a anexar nao existe.')
        warning = False
    
    #verificar se o proceso a ser anexado pertence a outra divisao
    if proc_anexo:
        divisao = Tbdivisao.objects.get(pk = Tbprocessobase.objects.get(nrprocesso = processoanexo).tbdivisao.id)
        if base.tbdivisao != divisao:
            messages.add_message(request_form, messages.WARNING, 'O processo a anexar existe,mas pertence a outra divisao.')
            warning = False        
    
    #verifica se o processo base eh classificado como processo pai
    if base.tbclassificacaoprocesso.id != 1:
        messages.add_message(request_form, messages.WARNING, 'Nao permitido anexar processo a processos classificados como anexos.')
        warning = False        
    #verifica se o anexo esta anexado a outro processo
    
    #verificar se ja foi anexado ao processo em questao    
    result = Tbprocessosanexos.objects.all().filter( tbprocessobase__id = base.id, tbprocessobase_id_anexo__nrprocesso = processoanexo )
    if result:
        messages.add_message(request_form, messages.WARNING, 'Processo '+processoanexo+' ja anexado.')
        warning = False
    return warning
    
def formatDataToText( formato_data ):
    if formato_data:
        if len(str(formato_data.day)) < 2:
            dtaberturaprocesso = '0'+str(formato_data.day)+"/"
        else:
            dtaberturaprocesso = str(formato_data.day)+"/"
        if len(str(formato_data.month)) < 2:
            dtaberturaprocesso += '0'+str(formato_data.month)+"/"
        else:
            dtaberturaprocesso += str(formato_data.month)+"/"
        dtaberturaprocesso += str(formato_data.year)
        return str( dtaberturaprocesso )
    else:
        return "";
    
def carregarTbAuxProcesso(request, tipo):
    global caixa, contrato, gleba, situacaogeo
    caixa = []
    gleba = []
    
    #for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == tipo:
            caixa.append( obj )
    sorted(caixa,key=lambda caixa: caixa.nmlocalarquivo)
       
    #gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    #carrega com as glebas da UF que o usuario pode acessar
    for obj in Tbgleba.objects.all().filter(tbuf__id__in=request.session['uf']).order_by('nmgleba'):
        gleba.append(obj)
    
    contrato = Tbcontrato.objects.all().filter( tbdivisao__id__in = request.session['divisoes']).order_by('nrcontrato')#AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nrcontrato')
    situacaogeo = Tbsituacaogeo.objects.all().order_by('nmsituacaogeo')#filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmsituacaogeo')
    
def carregarTbAuxFuncoesProcesso(request, base):
    global pendencia, tipopendencia, statuspendencia
    pendencia = Tbpendencia.objects.filter( tbprocessobase__id = base.id ).order_by('dsdescricao')
    tipopendencia = Tbtipopendencia.objects.all().order_by('dspendencia')#filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('dspendencia')
    statuspendencia = Tbstatuspendencia.objects.all().order_by("dspendencia")#filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by("dspendencia")

def prazo_notificacao_clausula( tpproc ):
    
    prazos = []
    if tpproc.tbprocessobase.tbetapaatual is not None:
        checksprazos = Tbchecklistprocessobase.objects.filter( tbprocessobase__id = tpproc.tbprocessobase.id, tbchecklist__tbetapa__id = tpproc.tbprocessobase.tbetapaatual.id,tbchecklist__bl_data_prazo = True, blnao_obrigatorio = False, blsanado = False )
        for obj in checksprazos:
            if obj.dtcustom is not None:
                if obj.tbchecklist.nrprazo is not None:
                    dias = obj.tbchecklist.nrprazo - (datetime.datetime.now() - obj.dtcustom).days
                    if dias >= 0 and dias <= 15:
                        prazos.append( dict({'obj':obj,'dias':dias}) )
    return prazos

def validarDesAnexo(request_form, base, processoanexo):
    global fgexiste 
    warning = True
    #verificar se campo processo a anexar esta em branco
    if processoanexo == '':
        messages.add_message(request_form, messages.WARNING, 'Numero do processo a ser desanexado nao informado')
        warning = False
    #verificar se processo a anexar eh o mesmo processo base
    if processoanexo == base.nrprocesso:
        messages.add_message(request_form, messages.WARNING, 'Processos iguais')
        warning = False
   
    #verificar se processo a anexar existe e pertence a divisao do usuario
    #proc_anexo = Tbprocessobase.objects.all().filter( nrprocesso = processoanexo)#, auth_user__tbdivisao = AuthUser.objects.get( pk = request_form.user.id ).tbdivisao )
    if not processoanexo:
        messages.add_message(request_form, messages.WARNING, 'O processo a desanexar nao existe.')
        warning = False
    
    #verificar se o proceso a ser anexado pertence a outra divisao
    if processoanexo:
        divisao = Tbdivisao.objects.get(pk = Tbprocessobase.objects.get(nrprocesso = processoanexo.nrprocesso).tbdivisao.id)
        if base.tbdivisao != divisao:
            messages.add_message(request_form, messages.WARNING, 'O processo a desanexar existe,mas pertence a outra divisao.')
    return warning
