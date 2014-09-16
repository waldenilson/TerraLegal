# coding: utf-8
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.tramitacao.models import Tbtipoprocesso, Tbprocessobase, Tbgleba, Tbmunicipio,\
    Tbcaixa, AuthUser, Tbprocessourbano, Tbsituacaoprocesso, Tbcontrato,\
    Tbsituacaogeo, Tbmovimentacao, Tbclassificacaoprocesso, Tbpregao, Tbdivisao,\
    Tbtransicao, Tbetapa, Tbchecklist, Tbchecklistprocessobase
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime
from django.db.models import Q

@permission_required('sicop.processo_urbano_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/processo/urbano/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('sicop.processo_urbano_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    pregao = Tbpregao.objects.all().order_by('nrpregao')
    
    carregarTbAuxProcesso(request)
      
    div_processo = "urbano"
    escolha = "tbprocessourbano" 
    
    if request.method == "POST":

        datatitulacao = None
        dataaberturaprocesso = None
        if request.POST['dttitulacao']:
            datatitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y")
        if request.POST['dtaberturaprocesso']:
            dataaberturaprocesso = datetime.datetime.strptime( request.POST['dtaberturaprocesso'], "%d/%m/%Y")
        
        if validacao(request, "cadastro"):
            # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-',''),
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessourbano' ),
                                    dtcadastrosistema = datetime.datetime.now(),
#                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()
                 
            area = request.POST['nrarea'].replace(',','.')
            if not area:
                area = None
                
            perimetro = request.POST['nrperimetro'].replace(',','.')
            if not perimetro:
                perimetro = None

            habitantes = request.POST['nrhabitantes'].replace(',','.')
            if not habitantes:
                habitantes = None
                
            domicilios = request.POST['nrdomicilios'].replace(',','.')
            if not domicilios:
                domicilios = None
            
            # cadastrando o registro processo urbano
            f_urbano = Tbprocessourbano (
                                       nmpovoado = request.POST['nmpovoado'],
                                       nrcnpj = request.POST['nrcnpj'].replace('.','').replace('/','').replace('-',''),
                                       nrhabitantes = habitantes,
                                       nrdomicilios = domicilios,
                                       tbpregao = Tbpregao.objects.get( pk = request.POST['tbpregao'] ),
                                       nrarea = area,
                                       nrperimetro = perimetro,
                                       dsprojetoassentamento = request.POST['dsprojetoassentamento'],
                                       tbsituacaogeo = Tbsituacaogeo.objects.get( pk = request.POST['tbsituacaogeo'] ),
                                       tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                       tbprocessobase = f_base,
                                       dtaberturaprocesso = dataaberturaprocesso,
                                       dttitulacao = datatitulacao,
                                       )
            f_urbano.save()
            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            
            return HttpResponseRedirect("/sicop/processo/consulta/")
           
    return render_to_response('sicop/processo/cadastro.html',
        {'tipoprocesso':tipoprocesso,'processo':escolha,'situacaoprocesso':situacaoprocesso, 
         'situacaogeo':situacaogeo,'pregao':pregao,'contrato':contrato,'gleba':gleba,'caixa':caixa,'municipio':municipio,'div_processo':div_processo},
         context_instance = RequestContext(request))     

@permission_required('sicop.processo_urbano_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    carregarTbAuxProcesso(request)
    pregao = Tbpregao.objects.all().order_by('nrpregao')
    
    urbano = get_object_or_404(Tbprocessourbano, id=id)
    base  = get_object_or_404(Tbprocessobase, id=urbano.tbprocessobase.id)

    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" )
    
    # caixa destino
    caixadestino = []
    #for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ):
    #    if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB' or obj.tbtipocaixa.nmtipocaixa == 'FT':
    #        caixadestino.append( obj )    
    for obj in Tbcaixa.objects.all().filter( Q(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )|Q(tbtipocaixa__nmtipocaixa__icontains='ENT')):
        if obj.tbtipocaixa.nmtipocaixa=='SER' or obj.tbtipocaixa.nmtipocaixa=='PAD' or obj.tbtipocaixa.nmtipocaixa=='FT' or obj.tbtipocaixa.nmtipocaixa=='ENT':
            caixadestino.append(obj)
   
    if validacao(request, "edicao"):
         # cadastrando o registro processo base            
            f_base = Tbprocessobase (
                                    id = base.id,
                                    nrprocesso = request.POST['tbprocessobase'].replace('.','').replace('-','').replace('/',''),,
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = base.tbcaixa,
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessourbano' ),
                                    dtcadastrosistema = base.dtcadastrosistema,
#                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                    tbdivisao = base.tbdivisao
                                    )
            f_base.save()
       
            datatitulacao = None
            dataaberturaprocesso = None
            if request.POST['dttitulacao']:
                datatitulacao = datetime.datetime.strptime( request.POST['dttitulacao'], "%d/%m/%Y")
            if request.POST['dtaberturaprocesso']:
                dataaberturaprocesso = datetime.datetime.strptime( request.POST['dtaberturaprocesso'], "%d/%m/%Y")
 
            area = request.POST['nrarea'].replace(',','.')
            if not area:
                area = None
                        
            perimetro = request.POST['nrperimetro'].replace(',','.')
            if not perimetro:
                perimetro = None

            habitantes = request.POST['nrhabitantes'].replace(',','.')
            if not habitantes:
                habitantes = None
                
            domicilios = request.POST['nrdomicilios'].replace(',','.')
            if not domicilios:
                domicilios = None
           
            # cadastrando o registro processo rural
            f_urbano = Tbprocessourbano (
                                       id = urbano.id,
                                       nmpovoado = request.POST['nmpovoado'],
                                       nrcnpj = request.POST['nrcnpj'].replace('.','').replace('/','').replace('-',''),
                                       nrhabitantes = habitantes,
                                       nrdomicilios = domicilios,
                                       nrarea = area,
                                       nrperimetro = perimetro,
                                       dsprojetoassentamento = request.POST['dsprojetoassentamento'],
                                       tbsituacaogeo = Tbsituacaogeo.objects.get( pk = request.POST['tbsituacaogeo'] ),
                                       tbpregao = Tbpregao.objects.get( pk = request.POST['tbpregao'] ),
                                       tbcontrato = Tbcontrato.objects.get( pk = request.POST['tbcontrato'] ),
                                       tbprocessobase = f_base,
                                       dtaberturaprocesso = dataaberturaprocesso,
                                       dttitulacao = datatitulacao,
                                       )
            f_urbano.save()

            #mudanca de etapa do processo / apenas quem possue permissao            
            if request.user.has_perm('sicop.etapa_checklist_edicao'):
                if request.POST['etapaposterior'] != '':

                    #salva todos os checklists obrigatorios
                    etapa_atual = transicao = Tbtransicao.objects.filter( tbprocessobase__id = urbano.tbprocessobase.id ).order_by('-dttransicao')[0]
                    checks_obrigatorios = Tbchecklist.objects.filter( tbetapa = etapa_atual.tbetapa, blobrigatorio = True )
                    for obj in checks_obrigatorios:
                        if not Tbchecklistprocessobase.objects.filter( tbchecklist__id = obj.id, tbprocessobase__id = base.id ):
                            cp = Tbchecklistprocessobase( tbprocessobase = Tbprocessobase.objects.get( pk = base.id ),
                                          tbchecklist = Tbchecklist.objects.get( pk = obj.id ) )
                            cp.save()

                    transicao = Tbtransicao(
                                     tbprocessobase = Tbprocessobase.objects.get( pk = base.id ) ,
                                     tbetapa = Tbetapa.objects.get( pk = request.POST['etapaposterior'] ),
                                     dttransicao = datetime.datetime.now()
                                    )                    
                    transicao.save()

            messages.add_message(request,messages.INFO,'Informações salvas com sucesso.')
            
            return HttpResponseRedirect("/sicop/processo/edicao/"+str(base.id)+"/")
           
    
    return render_to_response('sicop/processo/urbano/edicao.html',
                                   {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,'contrato':contrato,'situacaogeo':situacaogeo,
                                   'base':base,'movimentacao':movimentacao,'pregao':pregao,
                                   'caixadestino':caixadestino,'urbano':urbano}, context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if metodo == "cadastro":
        if request_form.POST['nrprocesso'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
            warning = False
    if request_form.POST['nrcnpj'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o CNPJ')
        warning = False
    if request_form.POST['nmpovoado'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do povoado')
        warning = False
    if request_form.POST['tbcontrato'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha o Contrato')
        warning = False
#    if request_form.POST['nrarea'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe a Area')
#        warning = False
#    if request_form.POST['nrperimetro'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe o Perimetro')
#        warning = False
#    if request_form.POST['nrhabitantes'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe o Numero de habitantes')
#        warning = False
#    if request_form.POST['nrdomicilios'] == '':
#        messages.add_message(request_form,messages.WARNING,'Informe o Numero de Domicilios')
#        warning = False
    if request_form.POST['tbpregao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Pregao')
        warning = False
    if request_form.POST['tbsituacaogeo'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma situacao GEO')
        warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
        warning = False
    if metodo == "cadastro":
        if request_form.POST['tbcaixa'] == '':
            messages.add_message(request_form,messages.WARNING,'Escolha uma caixa')
            warning = False
    if request_form.POST['dtaberturaprocesso'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a Data da abertura do processo')
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
    global caixa, gleba, situacaoprocesso, municipio, contrato, situacaogeo
    caixa = []
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'URB' or obj.tbtipocaixa.nmtipocaixa == 'FT' or obj.tbtipocaixa.nmtipocaixa == 'ENT':
            caixa.append( obj )
    gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    situacaoprocesso = Tbsituacaoprocesso.objects.all().order_by('nmsituacao')#filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmsituacao')
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )
    contrato = Tbcontrato.objects.all().filter( tbdivisao__id__in = request.session['divisoes']).order_by('nrcontrato') #AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nrcontrato')
    situacaogeo = Tbsituacaogeo.objects.all().order_by('nmsituacaogeo')#.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmsituacaogeo')

