from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from sicop.restrito import processo_rural
from sicop.relatorio_base import relatorio_base, relatorio_documento_base,\
    relatorio_base_consulta
from types import InstanceType
from sicop.admin import verificar_permissao_grupo, divisaoDoUsuarioLogado
import datetime
from django.contrib import messages

@login_required
def consulta(request):
    # carrega os processos da divisao do usuario logado
    lista = Tbprocessobase.objects.all().filter( auth_user__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by( "id" )
    if request.method == "POST":
        numero = request.POST['numero']
        cpf = request.POST['cpf']
        requerente = request.POST['requerente']
        cnpj = request.POST['cnpj']
        municipio = request.POST['municipio']
        
        if len(numero) > 0 :
            lista = Tbprocessobase.objects.all().filter( nrprocesso__contains = numero )
        
        if len(cpf) > 0 :
            p_rural = Tbprocessorural.objects.all().filter( nrcpfrequerente__contains = cpf )
            p_clausula = Tbprocessoclausula.objects.all().filter( nrcpfrequerente__contains = cpf )
            lista = []
            for obj in p_rural:
                lista.append( obj.tbprocessobase )
            for obj in p_clausula:
                lista.append( obj.tbprocessobase )
                
        if len(requerente) > 0 :
            p_rural = Tbprocessorural.objects.all().filter( nmrequerente__contains = requerente )
            p_clausula = Tbprocessoclausula.objects.all().filter( nmrequerente__contains = requerente )
            lista = []
            for obj in p_rural:
                lista.append( obj.tbprocessobase )
            for obj in p_clausula:
                lista.append( obj.tbprocessobase )
                
        if len(cnpj) > 0 :
            p_urbano = Tbprocessourbano.objects.all().filter( nrcnpj__contains = cnpj ) 
            lista = []
            for obj in p_urbano:
                lista.append( obj.tbprocessobase )

        if len(municipio) > 0 :
            p_urbano = Tbprocessourbano.objects.all().filter( nmpovoado__contains = municipio ) 
            lista = []
            for obj in p_urbano:
                lista.append( obj.tbprocessobase )    
    
    # gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_processo'] = lista
    
    # criar na sessao a divisao do usuario logado
    divisaoDoUsuarioLogado(request)
    
    return render_to_response('sicop/restrito/processo/consulta.html',{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
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
                                    tbsituacaoprocesso = base.tbsituacaoprocesso,
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    auth_user = base.auth_user,
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso
                                    )
            f_base.save()
            # criar registro da movimentacao
            f_movimentacao = Tbmovimentacao(
                                           tbprocessobase = base,
                                           tbcaixa_id = Tbcaixa.objects.get( pk = caixadestino),
                                           tbcaixa_id_origem = caixaorigem,
                                           auth_user = AuthUser.objects.get( pk = request.user.id ),
                                           dtmovimentacao = datetime.datetime.now()
                                           )
            f_movimentacao.save()
            
            #OBS ao tramitar o processo todos os processos anexados serao tramitados ( classificado como anexo )
                    
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
        caixa = Tbcaixa.objects.all()
        gleba = Tbgleba.objects.all() 
        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        contrato = Tbcontrato.objects.all()
        situacaogeo = Tbsituacaogeo.objects.all()
        situacaoprocesso = Tbsituacaoprocesso.objects.all()
        tipo = base.tbtipoprocesso.tabela
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = base.id ).order_by( "-dtmovimentacao" ) 
        # caixa destino
        caixadestino = Tbcaixa.objects.all()

        
        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'caixa':caixa,'municipio':municipio,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))

        

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all() 
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    contrato = Tbcontrato.objects.all()
    situacaogeo = Tbsituacaogeo.objects.all()
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
    
    base = get_object_or_404(Tbprocessobase, id=id)
    tipo = base.tbtipoprocesso.tabela
    
    
    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" ) 
    # caixa destino
    caixadestino = Tbcaixa.objects.all()
        
    # se processobase pertencer a mesma divisao do usuario logado
    if base.auth_user.tbdivisao.id == AuthUser.objects.get( pk = request.user.id ).tbdivisao.id:
        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'caixa':caixa,'municipio':municipio,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
        
    return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Operador'}), login_url='/excecoes/permissao_negada/')
#@permission_required('sicop.add tbprocesso', login_url='/sicop/acesso_restrito/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    escolha = "tbprocessorural"
    div_processo = "rural"
    caixa = Tbcaixa.objects.all()
    gleba = Tbgleba.objects.all()
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    contrato = Tbcontrato.objects.all()
    situacaogeo = Tbsituacaogeo.objects.all()
    situacaoprocesso = Tbsituacaoprocesso.objects.all()
           
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbprocessorural":
            div_processo = "rural"
            return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
        else:
            if escolha == "tbprocessourbano":
                div_processo = "urbano"
                return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo,'contrato':contrato,'situacaogeo':situacaogeo},
                    context_instance = RequestContext(request));  
            else:
                if escolha == "tbprocessoclausula":
                    div_processo = "clausula"
                    form = FormProcessoClausula()
                    return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'form':form,'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
       
    return render_to_response('sicop/restrito/processo/cadastro.html',{'gleba':gleba,'caixa':caixa,'municipio':municipio,'situacaoprocesso':situacaoprocesso,
            'tipoprocesso':tipoprocesso,'processo':escolha,'div_processo':div_processo}, context_instance = RequestContext(request))


def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_processo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS PROCESSOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/processo/consulta/")


def validarTramitacao(request_form, base, origem, destino):
    warning = True
    if  base.tbclassificacaoprocesso.id == 2:
        messages.add_message(request_form,messages.WARNING,'Processo Anexo nao pode ser tramitado.')
        warning = False
    if origem.id == Tbcaixa.objects.get( pk = destino).id:
        messages.add_message(request_form,messages.WARNING,'Processo ja encontra-se no local de destino.')
        warning = False    
    return warning
    
def formatDataToText( formato_data ):
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



