from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from sicop.restrito import processo_rural
from sicop.relatorio_base import relatorio_base, relatorio_documento_base,\
    relatorio_base_consulta
from types import InstanceType
from sicop.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages

@login_required
def consulta(request):
    # carrega os processos da divisao do usuario logado
    lista = []
    #lista = Tbprocessobase.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by( "id" )
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
            p_rural = Tbprocessorural.objects.all().filter( nmrequerente__icontains = requerente )
            p_clausula = Tbprocessoclausula.objects.all().filter( nmrequerente__icontains = requerente )
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
    # gravando na sessao a divisao do usuario logado
    request.session['divisao'] = AuthUser.objects.get( pk = request.user.id ).tbdivisao.nmdivisao +" - "+AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.nmuf
        
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
                                    tbdivisao = base.tbdivisao,
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso
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
            anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id )
            for nx in anexado:
                proc_anexado = nx.tbprocessobase_id_anexo
                f_base = Tbprocessobase (
                                        id = proc_anexado.id,
                                        nrprocesso = proc_anexado.nrprocesso,
                                        tbgleba = proc_anexado.tbgleba,
                                        tbmunicipio = proc_anexado.tbmunicipio,
                                        tbcaixa = Tbcaixa.objects.get( pk = caixadestino),
                                        tbtipoprocesso = proc_anexado.tbtipoprocesso,
                                        tbsituacaoprocesso = proc_anexado.tbsituacaoprocesso,
                                        dtcadastrosistema = proc_anexado.dtcadastrosistema,
                                        auth_user = proc_anexado.auth_user,
                                        tbdivisao = proc_anexado.tbdivisao,
                                        tbclassificacaoprocesso = proc_anexado.tbclassificacaoprocesso
                                        )
                f_base.save()
                    
            return HttpResponseRedirect("/sicop/restrito/processo/edicao/"+str(base.id)+"/")
        
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        tipo = base.tbtipoprocesso.tabela
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = base.id ).order_by( "-dtmovimentacao" ) 
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id )

        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            # caixas que podem ser tramitadas
            tram = []
            for obj in Tbcaixa.objects.all():
                if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD':
                    tram.append( obj )
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                # caixas que podem ser tramitadas
                tram = []
                for obj in Tbcaixa.objects.all():
                    if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB':
                        tram.append( obj )               
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    # caixas que podem ser tramitadas
                    tram = []
                    for obj in Tbcaixa.objects.all():
                        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB':
                            tram.append( obj )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))      

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def criar_pendencia(request, base):
    if request.method == "POST":
        
        base = get_object_or_404(Tbprocessobase, id=base )
        descricao = request.POST['dspendencia']
        if validarPendencia(request, base, descricao):
            
            f_pendencia = Tbpendencia(
                                      tbprocessobase = base,
                                      auth_user = AuthUser.objects.get( pk = request.user.id ),
                                      tbtipopendencia  = Tbtipopendencia.objects.get( pk = request.POST['tbtipopendencia'] ),
                                      tbstatuspendencia = Tbstatuspendencia.objects.get( pk = request.POST['tbstatuspendencia'] ) ,
                                      dsdescricao = descricao,
                                      dtpendencia = datetime.datetime.now()
                                      )
            f_pendencia.save()
                    
            return HttpResponseRedirect("/sicop/restrito/processo/edicao/"+str(base.id)+"/")
        
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        tipo = base.tbtipoprocesso.tabela
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = base.id ).order_by( "-dtmovimentacao" ) 
        # caixa destino
        caixadestino = Tbcaixa.objects.all()
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id )


        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))      

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def anexar(request, base):
    if request.method == "POST":
        
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
                                    tbsituacaoprocesso = proc_anexo.tbsituacaoprocesso,
                                    dtcadastrosistema = proc_anexo.dtcadastrosistema,
                                    auth_user = proc_anexo.auth_user,
                                    tbdivisao = base.tbdivisao,
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 2 )
                                    )
            f_anexo.save()
  
            
            return HttpResponseRedirect("/sicop/restrito/processo/edicao/"+str(base.id)+"/")
        
        carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
        carregarTbAuxFuncoesProcesso(request, base)

        tipo = base.tbtipoprocesso.tabela
        municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
        # movimentacoes deste processo
        movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = base.id ).order_by( "-dtmovimentacao" ) 
        # caixa destino
        caixadestino = Tbcaixa.objects.all()
        # anexos deste processo
        anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id )


        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = base.id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = base.id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = base.id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':caixadestino,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))      

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    base = get_object_or_404(Tbprocessobase, id=id)
    
    carregarTbAuxProcesso(request, base.tbcaixa.tbtipocaixa.nmtipocaixa)
    carregarTbAuxFuncoesProcesso(request, base)
    
    # municipios da divisao do usuario logado
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    tipo = base.tbtipoprocesso.tabela
    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" ) 
    # anexos deste processo
    anexado = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id )
    
    # se processobase pertencer a mesma divisao do usuario logado
    if base.auth_user.tbdivisao.id == AuthUser.objects.get( pk = request.user.id ).tbdivisao.id:
        if tipo == "tbprocessorural":
            rural = Tbprocessorural.objects.get( tbprocessobase = id )
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            # caixas que podem ser tramitadas
            tram = []
            for obj in Tbcaixa.objects.all():
                if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD':
                    tram.append( obj )
                
            return render_to_response('sicop/restrito/processo/rural/edicao.html',
                                      {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'base':base,'rural':rural,'peca':peca}, context_instance = RequestContext(request))
        else:
            if tipo == "tbprocessourbano":
                urbano = Tbprocessourbano.objects.get( tbprocessobase = id )
         
                dtaberturaprocesso = formatDataToText( urbano.dtaberturaprocesso )
                dttitulacao = formatDataToText( urbano.dttitulacao )
                # caixas que podem ser tramitadas
                tram = []
                for obj in Tbcaixa.objects.all():
                    if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB':
                        tram.append( obj )
                return render_to_response('sicop/restrito/processo/urbano/edicao.html',
                                          {'situacaoprocesso':situacaoprocesso,'gleba':gleba,'situacaogeo':situacaogeo,
                                       'caixa':caixa,'municipio':municipio,'contrato':contrato,
                                       'base':base,'urbano':urbano,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'dtaberturaprocesso':dtaberturaprocesso,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
            else:
                if tipo == "tbprocessoclausula":
                    clausula = Tbprocessoclausula.objects.get( tbprocessobase = id )
                    dttitulacao = formatDataToText( clausula.dttitulacao )
                    # caixas que podem ser tramitadas
                    tram = []
                    for obj in Tbcaixa.objects.all():
                        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'RES':
                            tram.append( obj )
                    return render_to_response('sicop/restrito/processo/clausula/edicao.html',
                                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                       'caixa':caixa,'municipio':municipio,'anexado':anexado,'pendencia':pendencia,
                                       'movimentacao':movimentacao,'caixadestino':tram,'tipopendencia':tipopendencia,'statuspendencia':statuspendencia,
                                       'base':base,'clausula':clausula,'dttitulacao':dttitulacao}, context_instance = RequestContext(request))
        
    return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Operador'}), login_url='/excecoes/permissao_negada/')
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
            return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
        else:
            if escolha == "tbprocessourbano":
                div_processo = "urbano"
                carregarTbAuxProcesso(request, 'URB')
                return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo,'contrato':contrato,'situacaogeo':situacaogeo},
                    context_instance = RequestContext(request));  
            else:
                if escolha == "tbprocessoclausula":
                    div_processo = "clausula"
                    form = FormProcessoClausula()
                    carregarTbAuxProcesso(request, 'RES')
                    return render_to_response('sicop/restrito/processo/cadastro.html',
                    {'form':form,'tipoprocesso':tipoprocesso,'situacaoprocesso':situacaoprocesso,'gleba':gleba,'caixa':caixa,'municipio':municipio,'processo':escolha,
                    'div_processo':div_processo},
                    context_instance = RequestContext(request));  
    carregarTbAuxProcesso(request, 'PAD')   
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

# metodos classe controle

def validarTramitacao(request_form, base, origem, destino):
    warning = True
    if  base.tbclassificacaoprocesso.id == 2:
        messages.add_message(request_form,messages.WARNING,'Processo Anexo nao pode ser tramitado.')
        warning = False
    if origem.id == Tbcaixa.objects.get( pk = destino).id:
        messages.add_message(request_form,messages.WARNING,'Processo ja encontra-se no local de destino.')
        warning = False    
    return warning

def validarPendencia(request_form, base, descricao):
    warning = True
    if descricao == '':
        messages.add_message(request_form, messages.WARNING, 'Informe a descricao da pendencia.')
        warning = False
    return warning

def validarAnexo(request_form, base, processoanexo):
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
    proc_anexo = Tbprocessobase.objects.all().filter( nrprocesso = processoanexo, auth_user__tbdivisao = AuthUser.objects.get( pk = request_form.user.id ).tbdivisao )
    if not proc_anexo:
        messages.add_message(request_form, messages.WARNING, 'O processo a anexar nao existe.')
        warning = False        
    #verifica se o processo base eh classificado como processo pai
    if base.tbclassificacaoprocesso.id != 1:
        messages.add_message(request_form, messages.WARNING, 'Nao permitido anexar processo a processos classificados como anexos.')
        warning = False        
    #verifica se o anexo esta anexado a outro processo
    
    #verificar se ja foi anexado ao processo em questao    
    result = Tbprocessosanexos.objects.all().filter( tbprocessobase = base.id, tbprocessobase_id_anexo__nrprocesso = processoanexo )
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
    global caixa, contrato, gleba, situacaoprocesso, situacaogeo
    caixa = []
    for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == tipo:
            caixa.append( obj )
    
    gleba = Tbgleba.objects.all().filter( tbsubarea__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    contrato = Tbcontrato.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    situacaogeo = Tbsituacaogeo.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    situacaoprocesso = Tbsituacaoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )

def carregarTbAuxFuncoesProcesso(request, base):
    global pendencia, tipopendencia, statuspendencia
    pendencia = Tbpendencia.objects.all().filter( tbprocessobase = base.id )
    tipopendencia = Tbtipopendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    statuspendencia = Tbstatuspendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by("id")


