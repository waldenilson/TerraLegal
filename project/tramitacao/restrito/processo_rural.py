# coding: utf-8
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from project.tramitacao.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbdivisao, Tbtransicao, Tbetapa,\
    Tbchecklist, Tbchecklistprocessobase
from project.documento.models import Sobreposicao, DespachoAprovacaoRegional
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime
from django.db.models import  Q
from os.path import abspath, join, dirname
from project import settings
from project.core.funcoes import gerar_pdf, emitir_documento,mes_do_ano_texto

@permission_required('sicop.processo_rural_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/processo/rural/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('sicop.processo_rural_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    carregarTbAuxProcesso(request)
    etapaprocesso = Tbetapa.objects.filter( blinicial = True, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ,tbtipoprocesso__id = 1 ).order_by('ordem')
    
    div_processo = "rural"
    escolha = "tbprocessorural"
    
    if request.method == "POST":
            
        #verifica se o cadastro tem conjuge
        tem_conjuge = False
        if request.POST['nmconjuge'] != '' and request.POST['nrcpfconjuge'] != '':
            tem_conjuge = True

        if validacao(request, "cadastro"):
            
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                                    nmendereco = request.POST['nmendereco'],
                                    nmcontato = request.POST['nmcontato'],
                                    )
            if request.POST['tbgleba'] != '0':
                f_base.tbgleba = Tbgleba.objects.get(pk = request.POST['tbgleba'])
            else:
                f_base.tbgleba = None

            if request.POST['tbmunicipio'] != '0':
                f_base.tbmunicipio = Tbmunicipio.objects.get(pk = request.POST['tbmunicipio'])
            else:
                f_base.tbmunicipio = None
                
            try:
                mun = request.POST['tbmunicipiodomicilio'].split(',',1)[0]
                sigla = request.POST['tbmunicipiodomicilio'].split(',',1)[1]
                f_base.tbmunicipiodomicilio = Tbmunicipio.objects.filter( nome_mun = mun, uf = sigla )[0]
            except:
                f_base.tbmunicipiodomicilio = None

            f_base.save()
            
            # cadastrando o registro processo rural
            f_rural = Tbprocessorural (
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmconjuge = request.POST['nmconjuge'],
                                       nrcpfconjuge = request.POST['nrcpfconjuge'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       blconjuge = tem_conjuge
                                       )
            f_rural.save()

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
        {'gleba':gleba,'etapaprocesso':etapaprocesso,'caixa':caixa,
        'municipio':municipio,'municipiodomicilio':Tbmunicipio.objects.all(),'tipoprocesso':tipoprocesso, 
        'processo':escolha, 'div_processo':div_processo}, context_instance = RequestContext(request))    

@permission_required('sicop.processo_rural_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    carregarTbAuxProcesso(request)    
    rural = get_object_or_404(Tbprocessorural, id=id)
    base  = get_object_or_404(Tbprocessobase, id=rural.tbprocessobase.id)
    #titulo = get_object_or_404(TbTitulo,id=base.tbtitulo)

    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.filter( tbprocessobase = id ).order_by( "-dtmovimentacao" )
    # caixa destino
    caixadestino = []
    #for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ):       
    #   if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD' or obj.tbtipocaixa.nmtipocaixa == 'FT':
    #        caixadestino.append( obj )
    for obj in Tbcaixa.objects.all().filter( Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )|Q(tbtipocaixa__nmtipocaixa__icontains='ENT')):
        if obj.tbtipocaixa.nmtipocaixa=='SER' or obj.tbtipocaixa.nmtipocaixa=='PAD' or obj.tbtipocaixa.nmtipocaixa=='FT' or obj.tbtipocaixa.nmtipocaixa=='ENT':
            caixadestino.append(obj)

    #verifica se o cadastro tem conjuge
    tem_conjuge = False
    if request.POST['nmconjuge'] != '' and request.POST['nrcpfconjuge'] != '':
        tem_conjuge = True

    if validacao(request, "edicao"):
         # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['tbprocessobase'].replace('.','').replace('-','').replace('/',''),
                                    tbgleba = base.tbgleba,
                                    tbmunicipio = base.tbmunicipio,
                                    tbcaixa = base.tbcaixa,
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
#                                    tbetapaatual = base.tbetapaatual,
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                    tbdivisao = base.tbdivisao,
                                    nmendereco = request.POST['nmendereco'],
                                    nmcontato = request.POST['nmcontato'],
                                    tbtitulo = base.tbtitulo
                                    
                                    )
            try:
                mun = request.POST['tbmunicipiodomicilio'].split(',',1)[0]
                sigla = request.POST['tbmunicipiodomicilio'].split(',',1)[1]
                f_base.tbmunicipiodomicilio = Tbmunicipio.objects.filter( nome_mun = mun, uf = sigla )[0]
            except:
                f_base.tbmunicipiodomicilio = base.tbmunicipiodomicilio

            f_base.save()
            
            # cadastrando o registro processo rural
            f_rural = Tbprocessorural (
                                       id = rural.id,
                                       nmrequerente = request.POST['nmrequerente'],
                                       nrcpfrequerente = request.POST['nrcpfrequerente'].replace('.','').replace('-',''),
                                       nmconjuge = request.POST['nmconjuge'],
                                       nrcpfconjuge = request.POST['nrcpfconjuge'].replace('.','').replace('-',''),
                                       tbprocessobase = f_base,
                                       blconjuge = tem_conjuge
                                       )
            f_rural.save()
            
            #mudanca de etapa do processo / apenas quem possue permissao            
            if request.user.has_perm('sicop.etapa_checklist_edicao'):
                # se o usuario selecionou uma etapa
                if request.POST['etapaposterior'] != '':

                    #salva todos os checklists obrigatorios
                    etapa_atual = Tbtransicao.objects.filter( tbprocessobase__id = rural.tbprocessobase.id ).order_by('-dttransicao')[0]
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
            
            return HttpResponseRedirect("/tramitacao/processo/edicao/"+str(base.id)+"/")

    return render_to_response('sicop/processo/rural/edicao.html',
                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,
                                   'base':base,'movimentacao':movimentacao,
                                   'sobreposicao':documento_sobreposicao,
                                   'municipiodomicilio':Tbmunicipio.objects.all(),'caixadestino':caixadestino,'rural':rural},
                               context_instance = RequestContext(request))   

@permission_required('sicop.processo_rural_sobreposicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def gerar_doc_sobreposicao(request, id):

    # emitir a verificacao de sobreposicao em pdf atraves do modelo em html.
    rural = Tbprocessorural.objects.get(pk=id)
    resp_12 = 'NÃO'
    if not request.POST['forma_geo'] == 'GEORREFERENCIAMENTO PARTICULAR':
        resp_12 = 'SIM'
    n_parcelas = ''
    if not request.POST['n_parcelas'][0] == '0':
        n_parcelas = '0'+request.POST['n_parcelas']
    else:
        n_parcelas = request.POST['n_parcelas']

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

    processo = rural.tbprocessobase.nrprocesso[0:5]+'.'+rural.tbprocessobase.nrprocesso[5:11]+'/'+rural.tbprocessobase.nrprocesso[11:15]+'-'+rural.tbprocessobase.nrprocesso[15:17]

    dados = {
                'brasao':abspath(join(dirname(__file__), '../../../staticfiles'))+'/img/brasao.gif',
                'data':str(dia)+'/'+str(mes)+'/'+str(datetime.datetime.now().year),
                'cpf_detentor':request.POST['cpf_detentor'],
                'nome_detentor':request.POST['nome_detentor'],
                'processo':processo,
                'nome_imovel':request.POST['nome_imovel'],
                'nome_municipio':request.POST['nome_municipio'],
                'uf':request.POST['uf'],
                'nome_gleba':request.POST['nome_gleba'],
                'area_imovel':request.POST['area_imovel'],
                'n_parcelas':n_parcelas,

                'resp_01':check_boolean(request,'resp_01'),
                'resp_02':check_boolean(request,'resp_02'),
                'resp_03':check_boolean(request,'resp_03'),
                'resp_04':check_boolean(request,'resp_04'),
                'resp_05':check_boolean(request,'resp_05'),
                'resp_06':check_boolean(request,'resp_06'),
                'resp_07':check_boolean(request,'resp_07'),
                'resp_08':check_boolean(request,'resp_08'),
                'resp_09':check_boolean(request,'resp_09'),
                'resp_10':check_boolean(request,'resp_10'),
                'resp_11':check_boolean(request,'resp_11'),
                'resp_12':resp_12,
                'resp_01_txt':request.POST['resp_01_txt'],
                'resp_02_txt':request.POST['resp_02_txt'],
                'resp_03_txt':request.POST['resp_03_txt'],
                'resp_04_txt':request.POST['resp_04_txt'],
                'resp_05_txt':request.POST['resp_05_txt'],
                'resp_06_txt':request.POST['resp_06_txt'],
                'resp_07_txt':request.POST['resp_07_txt'],
                'resp_08_txt':request.POST['resp_08_txt'],
                'resp_09_txt':request.POST['resp_09_txt'],
                'resp_10_txt':request.POST['resp_10_txt'],
                'resp_11_txt':request.POST['resp_11_txt'],
                'forma_geo':request.POST['forma_geo'],
                'data_atualizacao':request.POST['data_atualizacao']
            }

    #PERSISTENCIA DOS DADOS DO DOCUMENTO VERIFICACAO SOBREPOSICAO
    doc = Sobreposicao.objects.filter( tbprocessobase__id = Tbprocessorural.objects.get(pk=id).tbprocessobase.id )
    ds = Sobreposicao()    
    if doc:
        #Atualizar dados
        ds.id = Sobreposicao.objects.get(pk = doc[0].id).id
        ds.data_cadastro = doc[0].data_cadastro
    else:
        #Persistir dados
        ds.data_cadastro = datetime.datetime.now()
    ds.data_modificacao = datetime.datetime.now()        
    ds.auth_user = AuthUser.objects.get(pk=request.user.id)
    ds.tbprocessobase = Tbprocessorural.objects.get(pk=id).tbprocessobase
    dt = request.POST['data_atualizacao'].split('/')
    ds.data_atualizacao = datetime.datetime(day=int(dt[0]),month=int(dt[1]),year=int(dt[2]))
    ds.forma_georreferenciamento = request.POST['forma_geo']

    ds.bl_item_1 = request.POST.get('resp_01',False)
    ds.txt_item_1 = request.POST['resp_01_txt']
    ds.bl_item_2 = request.POST.get('resp_02',False)
    ds.txt_item_2 = request.POST['resp_02_txt']
    ds.bl_item_3 = request.POST.get('resp_03',False)
    ds.txt_item_3 = request.POST['resp_03_txt']
    ds.bl_item_4 = request.POST.get('resp_04',False)
    ds.txt_item_4 = request.POST['resp_04_txt']
    ds.bl_item_5 = request.POST.get('resp_05',False)
    ds.txt_item_5 = request.POST['resp_05_txt']
    ds.bl_item_6 = request.POST.get('resp_06',False)
    ds.txt_item_6 = request.POST['resp_06_txt']
    ds.bl_item_7 = request.POST.get('resp_07',False)
    ds.txt_item_7 = request.POST['resp_07_txt']
    ds.bl_item_8 = request.POST.get('resp_08',False)
    ds.txt_item_8 = request.POST['resp_08_txt']
    ds.bl_item_9 = request.POST.get('resp_09',False)
    ds.txt_item_9 = request.POST['resp_09_txt']
    ds.bl_item_10 = request.POST.get('resp_10',False)
    ds.txt_item_10 = request.POST['resp_10_txt']
    ds.bl_item_11 = request.POST.get('resp_11',False)
    ds.txt_item_11 = request.POST['resp_11_txt']

    ds.save()

    return gerar_pdf(request,'/tramitacao/processo/rural/sobreposicao.html',dados, settings.MEDIA_ROOT+'/tmp','sobreposicao.pdf')

@permission_required('sicop.processo_rural_despacho_aprovacao_regional', login_url='/excecoes/permissao_negada/', raise_exception=True)
def gerar_doc_despacho_aprovacao_regional(request, id):

    # emitir a verificacao de sobreposicao em pdf atraves do modelo em html.
    rural = Tbprocessorural.objects.get(pk=id)

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

    data_despacho = request.POST['data_despacho']

    processo = rural.tbprocessobase.nrprocesso[0:5]+'.'+rural.tbprocessobase.nrprocesso[5:11]+'/'+rural.tbprocessobase.nrprocesso[11:15]+'-'+rural.tbprocessobase.nrprocesso[15:17]

    dados = {
                'brasao':abspath(join(dirname(__file__), '../../../staticfiles'))+'/img/brasao.gif',
                'data':str(dia)+'/'+str(mes)+'/'+str(datetime.datetime.now().year),
                'cpf_detentor':request.POST['cpf_detentor'],
                'nome_detentor':request.POST['nome_detentor'],
                'processo':processo,
                'nome_imovel':request.POST['nome_imovel'],
                'nome_municipio':request.POST['nome_municipio'],
                'uf':request.POST['uf'],
                'nome_gleba':request.POST['nome_gleba'],
                'area_imovel':request.POST['area_imovel'],

                'numero':request.POST['numero_aprovacao_regional'],
                'assunto':request.POST['assunto_aprovacao_regional'],
                'cidade':request.POST['cidade_aprovacao_regional'],
                'ano':request.POST['ano_aprovacao_regional'],
                'folha':request.POST['folha_aprovacao_regional'],
                'dia_despacho': data_despacho.split('/')[0],
                'mes_despacho': mes_do_ano_texto(int(data_despacho.split('/')[1])),
                'ano_despacho': data_despacho.split('/')[2]
            }

    #PERSISTENCIA DOS DADOS DO DOCUMENTO VERIFICACAO SOBREPOSICAO
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
    
    return emitir_documento('despacho_aprovacao_regional.odt',dados)
    #return gerar_pdf(request,'/tramitacao/processo/rural/despacho_aprovacao_regional.html',dados, settings.MEDIA_ROOT+'/tmp','aprovacao_regional.pdf')

def check_boolean(request,name):
    if request.POST.get(name,False):
        return 'SIM'
    else:
        return 'NÃO'

def validacao(request_form, metodo):
    warning = True
    if metodo == "cadastro":        
        if request_form.POST['nrprocesso'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
            warning = False
    if request_form.POST['nmrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do requerente')
        warning = False
    if request_form.POST['nrcpfrequerente'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CPF do requerente')
        warning = False
    if metodo == "cadastro":        
        if request_form.POST['tbcaixa'] == '':
            messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
            warning = False
    #if metodo == "cadastro":        
    #    if request_form.POST['tbsituacaoprocesso'] == '':
    #        messages.add_message(request_form,messages.WARNING,'Escolha a situacao do processo')
    #        warning = False
    
    # validacao dos dados de conjuge
    if request_form.POST['nmconjuge'] != '' and request_form.POST['nrcpfconjuge'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe os dados do conjuge corretamente')
        warning = False
    else:
        if request_form.POST['nmconjuge'] == '' and request_form.POST['nrcpfconjuge'] != '':
            messages.add_message(request_form,messages.WARNING,'Informe os dados do conjuge corretamente')
            warning = False
    
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
    #for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD' or obj.tbtipocaixa.nmtipocaixa == 'FT':
            caixa.append( obj )
    gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )

