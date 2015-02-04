# coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.tramitacao.models import Tbtipoprocesso, Tbmunicipio, Tbgleba, Tbcaixa,\
    Tbprocessobase, AuthUser, Tbprocessoclausula, Tbclassificacaoprocesso,\
    Tbsituacaoprocesso, Tbmovimentacao, Tbdivisao, Tbtransicao, Tbetapa,\
    Tbchecklist, Tbchecklistprocessobase
from TerraLegal.tramitacao.forms import FormProcessoClausula
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime

@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def notificacao(request):
    prazos = []
    consulta = []
    checksprazos = Tbchecklistprocessobase.objects.filter( tbchecklist__bl_data_prazo = True, blnao_obrigatorio = False, blsanado = False ).order_by('tbprocessobase')
    for obj in checksprazos:
        if obj.dtcustom is not None:
            dias = (obj.dtcustom - datetime.datetime.now()).days
            if dias >= 0 and dias <= 15:
                prazos.append( dict({'obj':obj,'dias':dias}) )        
    if prazos:
        for op in prazos:
            proc = Tbprocessoclausula.objects.filter( tbprocessobase__id = op['obj'].tbprocessobase.id )
            consulta.append( dict({'proc':proc[0],'check':op['obj'].tbchecklist.nmchecklist,'etapa':op['obj'].tbchecklist.tbetapa.nmfase,'dias':op['dias']}) )
    return render_to_response('sicop/processo/clausula/prazo_notificacao.html',{'consulta':consulta}, context_instance = RequestContext(request))    


@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/processo/clausula/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('sicop.processo_clausula_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    
    tipoprocesso = Tbtipoprocesso.objects.all()
    etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 2 ).order_by('ordem')
    
    carregarTbAuxProcesso(request)
    

    procuracao = False
    if request.POST.get('stprocuracao',False):
        procuracao = True

    liberacao = False
    if request.POST.get('stcertliberacao',False):
        liberacao = True

    quitacao = False
    if request.POST.get('stcertquitacao',False):
        quitacao = True
            
    div_processo = "clausula"
    escolha = "tbprocessoclausula"  
    
    if request.method == "POST":

        if validacao(request, "cadastro"):
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessoclausula' ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                                    nmendereco = request.POST['nmendereco'],
                                    nmcontato = request.POST['nmcontato'],                                    
                                    )

            try:
                f_base.tbmunicipiodomicilio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipiodomicilio'])
            except:
                f_base.tbmunicipiodomicilio = None

            f_base.save()
            
            # cadastrando o registro processo rural
            f_clausula = Tbprocessoclausula (
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmtitulo = request.POST['nmtitulo'],
                                       tptitulo = request.POST['tptitulo'],
                                       nmimovel = request.POST['nmimovel'],
                                       nmloteimovel = request.POST['nmloteimovel'],
                                       nminteressado = request.POST['nminteressado'],
                                       nrcpfinteressado = request.POST['nrcpfinteressado'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       nrarea = request.POST['nrarea'].replace(',','.'),
                                       stprocuracao = procuracao,
                                       dsobs = request.POST['dsobs'],
                                       dsprioridade = request.POST['dsprioridade'],
                                       stcertquitacao = quitacao,
                                       stcertliberacao = liberacao,
                                       blgeoimovel = request.POST.get('blgeoimovel',False)
                                       )

            try:
                f_clausula.dttitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y")
            except:
                f_clausula.dttitulacao = None

            try:
                f_clausula.dtrequerimento = datetime.datetime.strptime( request.POST['dtrequerimento'], "%d/%m/%Y")
            except:
                f_clausula.dtrequerimento = None

            try:
                f_clausula.dtnascimento = datetime.datetime.strptime( request.POST['dtnascimento'], "%d/%m/%Y")
            except:
                f_clausula.dtnascimento = None

            f_clausula.save()

            #escolheu uma etapa inicial
            if request.POST['etapainicial'] != '':
                transicao = Tbtransicao(
                    tbprocessobase = f_base ,
                    tbetapa = Tbetapa.objects.get( pk = request.POST['etapainicial'] ),
                    dttransicao = datetime.datetime.now(),
                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                )
                transicao.save()

                f_base.tbetapaatual = transicao.tbetapa
                f_base.save()

            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            
            return HttpResponseRedirect("/sicop/processo/consulta/")
    
    return render_to_response('sicop/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso,'etapaprocesso':etapaprocesso,'processo':escolha, 'gleba':gleba,'caixa':caixa,'municipio':municipio,'div_processo':div_processo},
         context_instance = RequestContext(request))     

@permission_required('sicop.processo_clausula_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    
    carregarTbAuxProcesso(request)
 
    procuracao = False
    if request.POST.get('stprocuracao',False):
        procuracao = True
    quitacao = False
    if request.POST.get('stcertquitacao',False):
        quitacao = True
    liberacao = False
    if request.POST.get('stcertliberacao',False):
        liberacao = True
    
    clausula = get_object_or_404(Tbprocessoclausula, id=id)
    base  = get_object_or_404(Tbprocessobase, id=clausula.tbprocessobase.id)
 


        # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" )
    
    # caixa destino
    caixadestino = []
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'RES' or obj.tbtipocaixa.nmtipocaixa == 'FT':
            caixadestino.append( obj )    

    if validacao(request, "edicao"):
        # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['tbprocessobase'].replace('.','').replace('-','').replace('/',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = base.tbcaixa,
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessoclausula' ),
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    tbetapaatual = base.tbetapaatual,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                    nmcontato = request.POST['nmcontato'],
                                    nmendereco = request.POST['nmendereco'],
                                    tbdivisao = base.tbdivisao,
                                    )
            try:
                f_base.tbmunicipiodomicilio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipiodomicilio'])
            except:
                f_base.tbmunicipiodomicilio = None
            f_base.save()
            
            # cadastrando o registro processo clausula
            f_clausula = Tbprocessoclausula (
                                       id = clausula.id,
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmtitulo = request.POST['nmtitulo'],
                                       tptitulo = request.POST['tptitulo'],
                                       nmimovel = request.POST['nmimovel'],
                                       nmloteimovel = request.POST['nmloteimovel'],
                                       nminteressado = request.POST['nminteressado'],
                                       nrcpfinteressado = request.POST['nrcpfinteressado'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       nrarea = request.POST['nrarea'].replace(',','.'),
                                       stprocuracao = procuracao,
                                       dsobs = request.POST['dsobs'],
                                       dsprioridade = request.POST['dsprioridade'],
                                       stcertquitacao = quitacao,
                                       stcertliberacao = liberacao,
                                       blgeoimovel = request.POST.get('blgeoimovel',False),
                                       blemprogramacao = request.POST.get('blemprogramacao',False)
                                       )

            print request.POST['dtnascimento']
            try:
                f_clausula.dtnascimento = request.POST['dtnascimento']#datetime.datetime.strptime( request.POST['dtnascimento'], "%d/%m/%Y")
            except:
                f_clausula.dtnascimento = None

            try:
                f_clausula.dtrequerimento = datetime.datetime.strptime( request.POST['dtrequerimento'], "%d/%m/%Y")
            except:
                f_clausula.dtrequerimento = None

            try:
                f_clausula.dttitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y")
            except:
                f_clausula.dttitulacao = None
            

            f_clausula.save()
            
            #mudanca de etapa do processo / apenas quem possue permissao            
            if request.user.has_perm('sicop.etapa_checklist_edicao'):
                if request.POST['etapaposterior'] != '':

                                        #salva todos os checklists obrigatorios
                    etapa_atual = transicao = Tbtransicao.objects.filter( tbprocessobase__id = clausula.tbprocessobase.id ).order_by('-dttransicao')[0]
                    checks_obrigatorios = Tbchecklist.objects.filter( tbetapa = etapa_atual.tbetapa, blobrigatorio = True )
                    for obj in checks_obrigatorios:
                        if not Tbchecklistprocessobase.objects.filter( tbchecklist__id = obj.id, tbprocessobase__id = base.id ):
                            cp = Tbchecklistprocessobase( tbprocessobase = Tbprocessobase.objects.get( pk = base.id ),
                                          tbchecklist = Tbchecklist.objects.get( pk = obj.id ) )
                            cp.save()

                    transicao = Tbtransicao(
                                     tbprocessobase = Tbprocessobase.objects.get( pk = base.id ) ,
                                     tbetapa = Tbetapa.objects.get( pk = request.POST['etapaposterior'] ),
                                     dttransicao = datetime.datetime.now(),
                                     auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    )                    
                    transicao.save()

                    f_base.tbetapaatual = transicao.tbetapa
                    f_base.save()

            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
        
    return render_to_response('sicop/processo/clausula/edicao.html',
                                          {'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,'movimentacao':movimentacao,
                                   'caixadestino':caixadestino,
                                   'base':base,'clausula':clausula}, context_instance = RequestContext(request))    

def validacao(request_form, metodo):
    warning = True
    if metodo == "cadastro":
        if request_form.POST['nrprocesso'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
            warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do titulado')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CPF do titulado')
        warning = False
    if metodo == "cadastro":
        if request_form.POST['tbcaixa'] == '':
            messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
            warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
        warning = False
    if request_form.POST['nrarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero da area')
        warning = False
#    if request_form.POST['dttitulacao'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe a data de titulacao')
#        warning = False
        
    if metodo == "cadastro":    
        if nrProcessoCadastrado( request_form.POST['nrprocesso'].replace('.','').replace('/','').replace('-','') ):
            messages.add_message(request_form,messages.WARNING,'Numero deste processo ja cadastrado')
            warning = False

    return warning

def nrProcessoCadastrado( numero ):
    result = Tbprocessobase.objects.all().filter( nrprocesso = numero )
    if result:
        return True
    else:
        return False

def carregarTbAuxProcesso(request):
    global caixa, gleba, municipio
    caixa = []
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'RES' or obj.tbtipocaixa.nmtipocaixa == 'FT':
            caixa.append( obj )
    #gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    gleba = Tbgleba.objects.all().filter( tbuf__id__in = request.session['uf'])
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )

