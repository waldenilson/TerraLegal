from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbdivisao, Tbtransicao, Tbetapa,\
    Tbchecklist, Tbchecklistprocessobase
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime
from django.db.models import  Q

@permission_required('sicop.processo_rural_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/processo/rural/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('sicop.processo_rural_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all()
    
    carregarTbAuxProcesso(request)    
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
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = Tbcaixa.objects.get( pk = request.POST['tbcaixa'] ),
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
#                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    dtcadastrosistema = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = Tbclassificacaoprocesso.objects.get( pk = 1 ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao,
                                    nmendereco = request.POST['nmendereco'],
                                    nmcontato = request.POST['nmcontato']
                                    )
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
            
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
        
    return render_to_response('sicop/restrito/processo/cadastro.html',
        {'gleba':gleba,'situacaoprocesso':situacaoprocesso,'caixa':caixa,'municipio':municipio,'tipoprocesso':tipoprocesso, 'processo':escolha, 'div_processo':div_processo}, context_instance = RequestContext(request))    

@permission_required('sicop.processo_rural_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    
    carregarTbAuxProcesso(request)    
    rural = get_object_or_404(Tbprocessorural, id=id)
    base  = get_object_or_404(Tbprocessobase, id=rural.tbprocessobase.id)
    
    # movimentacoes deste processo
    movimentacao = Tbmovimentacao.objects.all().filter( tbprocessobase = id ).order_by( "-dtmovimentacao" )
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
                                    tbgleba = Tbgleba.objects.get( pk = request.POST['tbgleba'] ),
                                    tbmunicipio = Tbmunicipio.objects.get( pk = request.POST['tbmunicipio'] ),
                                    tbcaixa = base.tbcaixa,
                                    tbtipoprocesso = Tbtipoprocesso.objects.get( tabela = 'tbprocessorural' ),
#                                    tbsituacaoprocesso = Tbsituacaoprocesso.objects.get( pk = request.POST['tbsituacaoprocesso'] ),
                                    dtcadastrosistema = base.dtcadastrosistema,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbclassificacaoprocesso = base.tbclassificacaoprocesso,
                                    tbdivisao = base.tbdivisao,
                                    nmendereco = request.POST['nmendereco'],
                                    nmcontato = request.POST['nmcontato']
                                    )
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
                                     dttransicao = datetime.datetime.now()
                                    )                    
                    transicao.save()
                               
            
            return HttpResponseRedirect("/sicop/restrito/processo/edicao/"+str(base.id)+"/")
    
    return render_to_response('sicop/restrito/processo/rural/edicao.html',
                              {'situacaoprocesso':situacaoprocesso,'gleba':gleba,
                                   'caixa':caixa,'municipio':municipio,
                                   'base':base,'movimentacao':movimentacao,
                                   'caixadestino':caixadestino,'rural':rural},
                               context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if metodo == "cadastro":        
        if request_form.POST['nrprocesso'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe o numero do processo')
            warning = False
    if request_form.POST['tbgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha uma gleba')
        warning = False
    if request_form.POST['tbmunicipio'] == '':
        messages.add_message(request_form,messages.WARNING,'Escolha um municipio')
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
    if metodo == "cadastro":        
        if request_form.POST['tbsituacaoprocesso'] == '':
            messages.add_message(request_form,messages.WARNING,'Escolha a situacao do processo')
            warning = False
    
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
    global caixa, gleba, situacaoprocesso, municipio
    caixa = []
    #for obj in Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
    for obj in Tbcaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmlocalarquivo'):
        if obj.tbtipocaixa.nmtipocaixa == 'SER' or obj.tbtipocaixa.nmtipocaixa == 'PAD' or obj.tbtipocaixa.nmtipocaixa == 'FT':
            caixa.append( obj )
    gleba = Tbgleba.objects.all().filter( tbuf__id = Tbdivisao.objects.get( pk = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).tbuf.id ).order_by('nmgleba')
    situacaoprocesso = Tbsituacaoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmsituacao')
    municipio = Tbmunicipio.objects.all().filter( codigo_uf = AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.id ).order_by( "nome_mun" )

