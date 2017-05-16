# coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.models import Tbtipoprocesso, Tbmunicipio, Tbgleba, Tbcaixa,\
    Tbprocessobase, Tbloganalise, AuthUser, Tbprocessoclausula, Tbclassificacaoprocesso,\
    Tbsituacaoprocesso, Tbmovimentacao, Tbdivisao, Tbtransicao, Tbetapa,\
    Tbchecklist, Tbchecklistprocessobase
from project.tramitacao.forms import FormProcessoClausula
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime
from os.path import abspath, join, dirname
from project.core.funcoes import upload_file
from pyexcel_ods import get_data
import json
from project.core.funcoes import gerar_pdf, emitir_documento,mes_do_ano_texto


@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/processo/clausula/consulta.html',{}, context_instance = RequestContext(request))    

@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def programacao_p80(request):
    consulta = []
    checks = Tbchecklistprocessobase.objects.filter( tbprocessobase__tbtipoprocesso__id = 2, tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id, bl_em_programacao = True, tbchecklist__blprogramacao = True ).order_by('tbprocessobase')
    for c in checks:
        consulta.append( Tbprocessoclausula.objects.filter(tbprocessobase__id = c.tbprocessobase.id)[0] )
    return render_to_response('sicop/processo/clausula/programacao_p80.html',{'consulta':consulta}, context_instance = RequestContext(request))    

@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def notificacao(request):
    prazos = []
    consulta = []
    checksprazos = Tbchecklistprocessobase.objects.filter( tbchecklist__bl_data_prazo = True, blnao_obrigatorio = False, blsanado = False ).order_by('tbprocessobase')
    for obj in checksprazos:
        if obj.dtcustom is not None:
            if obj.tbchecklist.nrprazo is not None:
                dias = obj.tbchecklist.nrprazo - (datetime.datetime.now() - obj.dtcustom).days
                if dias >= 0 and dias <= 15:
                    prazos.append( dict({'obj':obj,'dias':dias}) )        
    if prazos:
        for op in prazos:
            proc = Tbprocessoclausula.objects.filter( tbprocessobase__id = op['obj'].tbprocessobase.id )
            consulta.append( dict({'proc':proc[0],'check':op['obj'].tbchecklist.nmchecklist,'etapa':op['obj'].tbchecklist.tbetapa.nmfase,'dias':op['dias']}) )
    return render_to_response('sicop/processo/clausula/prazo_notificacao.html',{'consulta':consulta}, context_instance = RequestContext(request))    

@permission_required('sicop.processo_clausula_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def analise(request):
    etapas = Tbetapa.objects.filter( tbtipoprocesso__id = 2 ).order_by( 'ordem', 'nmfase' )
    consulta = []
    if request.method == 'POST':
        etapa = request.POST['etapa']

        res = Tbprocessoclausula.objects.filter(
            tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id, tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbetapaatual__id = etapa
            ).order_by('dtnascimento')
        for obj in res:
            if obj.dtnascimento is not None:
                if ((datetime.datetime.now().date() - obj.dtnascimento ).days)/365 >= 60:
                    consulta.append( obj )

        res = Tbprocessoclausula.objects.filter(
            tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id, tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbetapaatual__id = etapa
            ).order_by('dtrequerimento')
        for obj in res:
            if obj.dtnascimento is not None:
                if ((datetime.datetime.now().date() - obj.dtnascimento ).days)/365 < 60:
                    consulta.append( obj )
            else:
                consulta.append(obj)

    return render_to_response('sicop/processo/clausula/analise.html',{'consulta':consulta,'etapas':etapas}, context_instance = RequestContext(request))    
    
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

            if request.POST['tbgleba'] != '0':
                f_base.tbgleba = Tbgleba.objects.get(pk = request.POST['tbgleba'])
            else:
                f_base.tbgleba = None

            if request.POST['tbmunicipio'] != '0':
                f_base.tbmunicipio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipio'])
            else:
                f_base.tbmunicipio = None

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
            
            return HttpResponseRedirect("/tramitacao/processo/consulta/")
    
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

            if request.POST['tbgleba'] != '0':
                f_base.tbgleba = Tbgleba.objects.get(pk = request.POST['tbgleba'])
            else:
                f_base.tbgleba = None

            if request.POST['tbmunicipio'] != '0':
                f_base.tbmunicipio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipio'])
            else:
                f_base.tbmunicipio = None

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
                                       blgeoimovel = request.POST.get('blgeoimovel',False)
                                       )

            try:
                f_clausula.dtnascimento = datetime.datetime.strptime( request.POST['dtnascimento'], "%d/%m/%Y")
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


            # Se foi marcado que o processo foi analisado; salvar o log de analise
            if request.POST.get('analisado', False):
                analise = Tbloganalise(
                        dtanalise = datetime.datetime.now(),
                        tbprocessobase = base,
                        tbetapa = base.tbetapaatual,
                        tbcaixa = base.tbcaixa,
                        auth_user = AuthUser.objects.get( pk = request.user.id )
                )
                analise.save()

            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            
            return HttpResponseRedirect("/tramitacao/processo/edicao/"+str(base.id)+"/")
        
    return render_to_response('sicop/processo/clausula/edicao.html',
                                          {'gleba':gleba,'analises':Tbloganalise.objects.filter( tbprocessobase__id = base.id ).order_by('dtanalise'),
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


@permission_required('sicop.processo_clausula_pedido_cancelamento', login_url='/excecoes/permissao_negada/', raise_exception=True)
def gerar_pedido_cancelamento(request, id):
    print 'gerar_pedido_cancelamento'
    clausula = Tbprocessoclausula.objects.get(pk=id)
    municipio_cartorio = Tbmunicipio.objects.get(pk=request.POST['municipio_cartorio'])
    municipio_imovel = Tbmunicipio.objects.get(pk=request.POST['municipio_imovel'])

    dia = ''
    if datetime.datetime.now().day < 10:
        dia = '0'+str(datetime.datetime.now().day)
    else:
        dia = datetime.datetime.now().day

    mes = ''
    if datetime.datetime.now().month < 10:
        mes = '0'+str(datetime.datetime.now().month)
    else:
        mes = datetime.datetime.now().month

    data_oficio = request.POST['data_oficio']

    processo = clausula.tbprocessobase.nrprocesso[0:5]+'.'+clausula.tbprocessobase.nrprocesso[5:11]+'/'+clausula.tbprocessobase.nrprocesso[11:15]+'-'+clausula.tbprocessobase.nrprocesso[15:17]
    
    dados = {
                'brasao':abspath(join(dirname(__file__), '../../../staticfiles'))+'/img/brasao.gif',
                'data':str(dia)+'/'+str(mes)+'/'+str(datetime.datetime.now().year),
                #'cpf_detentor':request.POST['cpf_detentor'],
                'nome_interessado':request.POST['nome_interessado'],
                'processo':processo,
                'nome_imovel':request.POST['nome_imovel'],
                'municipio_imovel':municipio_imovel.nome_mun,
                'uf':request.POST['uf'],
                'nome_gleba':request.POST['nome_gleba'],
                'area_imovel':request.POST['area_imovel'],
                
                #'numero_oficio':request.POST['numero_oficio'],
                'ano_oficio':request.POST['ano_oficio'],
                'assunto':request.POST['assunto_cancelamento'],
                
                              
                'matricula':request.POST['matricula'],
                'livro':request.POST['livro'],
                'folhas':request.POST['folhas'],
                'dia_despacho': data_oficio.split('/')[0],
                'mes_despacho': mes_do_ano_texto(int(data_oficio.split('/')[1])),
                'ano_despacho': data_oficio.split('/')[2],
                'local_oficio': request.POST['local_oficio'],
                'data_matricula': request.POST['data_matricula'],
              
               
              
                'nome_cartorio':request.POST['nome_cartorio'], 
                'nome_titular': request.POST['nome_titular'],
                'nome_substituto': request.POST['nome_substituto'],
                'end_carto_1': request.POST['endereco_cartorio_1'],
                'cep': request.POST['cep'],
                'telefone': request.POST['telefone'],
                'mail': request.POST['mail'],
                'municipio': municipio_cartorio.nome_mun,                


                'data_expedicao_titulo':request.POST['data_expedicao_titulo'],
                'boletim_servico':request.POST['boletim_servico'],
                'lote':request.POST['lote']
                #'link':request.POST['link']

            }

    #PERSISTENCIA DOS DADOS DO DOCUMENTO VERIFICACAO SOBREPOSICAO
    #descomentar
    '''
    doc = DespachoAprovacaoRegional.objects.filter( tbprocessobase__id = Tbprocessorural.objects.get(pk=id).tbprocessobase.id )
    ds = DespachoAprovacaoRegional()
    if doc:
        #Atualizar dados
        ds.id = DespachoAprovacaoRegional.objects.get(pk = doc[0].id).id
        ds.data_cadastro = doc[0].data_cadastro
    else:
        #Persistir dados
        ds.data_cadastro = datetime.datetime.now()
    ds.data_despacho = datetime.datetime.now()
    ds.auth_user = AuthUser.objects.get(pk=request.user.id)
    ds.tbprocessobase = Tbprocessorural.objects.get(pk=id).tbprocessobase
    dt = request.POST['data_despacho'].split('/')
    ds.assunto = request.POST['assunto_aprovacao_regional']
    ds.data_atualizacao = datetime.datetime(day=int(dt[0]),month=int(dt[1]),year=int(dt[2]))
    ds.cidade = request.POST['cidade_aprovacao_regional']
    ds.numero = request.POST['numero_aprovacao_regional']
    ds.ano = request.POST['ano_aprovacao_regional']
    ds.folha = request.POST['folha_aprovacao_regional']
    ds.save()
    '''
    return emitir_documento('pedido_cancelamento_matricula.odt',dados)
    #return gerar_pdf(request,'/tramitacao/processo/rural/despacho_aprovacao_regional.html',dados, settings.MEDIA_ROOT+'/tmp','aprovacao_regional.pdf')
