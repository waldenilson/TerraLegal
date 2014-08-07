
# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbtipodocumento, Tbdocumentobase,\
    Tbservidor, Tbdocumentoservidor, Tbdocumentovr
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
import datetime
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import time
from reportlab.platypus.doctemplate import SimpleDocTemplate
import webodt
from TerraLegal import settings
from django.core.files.storage import default_storage
from webodt.shortcuts import render_to
from webodt import shortcuts
from sicop.admin import mes_do_ano_texto
from sicop.restrito.documento import formatDataToText

@permission_required('servidor.documento_requisicao_viatura_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/documento/requisicao_viatura/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('servidor.documento_requisicao_viatura_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    div_documento = "requisicao_viatura"
    escolha = "tbdocumentovr"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):

            # validando campos para uso no formato datetime do atributo datainicio dos servicos
            hrinicio = request.POST['horainicio']
            mininicio = request.POST['mininicio']
            if hrinicio == '':
                hrinicio = '00'
            if mininicio == '':
                mininicio = '00'

            servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            dtinicio = datetime.datetime.strptime( request.POST['dtinicio']+" "+hrinicio+":"+mininicio , "%d/%m/%Y %H:%M")
            dtsolicitante = datetime.datetime.strptime( request.POST['dtsolicitante'], "%d/%m/%Y")
            dtautorizado = None
            if request.POST['dtautorizado']:
                dtautorizado = datetime.datetime.strptime( request.POST['dtautorizado'], "%d/%m/%Y")
            
            # cadastrando o registro processo base            
            f_base = Tbdocumentobase (
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentovr' ),
                                    dtdocumento = dtsolicitante,
                                    dtcadastrodocumento = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()
            
            f_requisicao_viatura = Tbdocumentovr (
                                       objetivo = request.POST['objetivo'],
                                       destino = request.POST['destino'],
                                       tempodias = request.POST['tempodias'],
                                       motorista = request.POST['motorista'],
                                       usuarios = request.POST['usuarios'],
                                       localviatura = request.POST['localviatura'],
                                       dtinicioservicos = dtinicio,
                                       dtsolicitante = dtsolicitante,
                                       dtautorizado = dtautorizado,
                                       veiculo = request.POST['veiculo'],
                                       placa = request.POST['placa'],
                                       tbdocumentobase = f_base,
                                       )
            f_requisicao_viatura.save()

            for obj in servidor:
                if request.POST.get(obj.nmservidor, False):
                    #verificar se esse grupo ja esta ligado ao usuario
                        # inserir ao authusergroups
                    ug = Tbdocumentoservidor( tbdocumentobase = Tbdocumentobase.objects.get( pk = f_base.id ),
                                              tbservidor = Tbservidor.objects.get( pk = obj.id ) )
                    ug.save()
    
            return HttpResponseRedirect("/sicop/restrito/documento/consulta/")
        
    return render_to_response('sicop/restrito/documento/cadastro.html',
        {'tipodocumento':tipodocumento, 'documento':escolha, 'div_documento':div_documento}, context_instance = RequestContext(request))    

@permission_required('servidor.documento_requisicao_viatura_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criacao(request, id):   
        
    obj = get_object_or_404(Tbdocumentovr, id=id)
    
    dataservicos = formatDataToText(obj.dtinicioservicos)
    dtsol = formatDataToText(obj.dtsolicitante)
    dtauto = formatDataToText(obj.dtautorizado)
    hrservicos = str(obj.dtinicioservicos.hour)+":"+str(obj.dtinicioservicos.minute)+"h"
    
    return shortcuts.render_to_response('rv.odt',
                                        dictionary=dict( rv = obj, dataservicos = dataservicos, datasolicitante = dtsol, dataautorizado = dtauto, horaservicos = hrservicos ),
                                        format='odt',filename=str(obj.tbdocumentobase.nmdocumento)+'.odt')
            
@permission_required('servidor.documento_requisicao_viatura_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
        
    requisicao_viatura = get_object_or_404(Tbdocumentovr, id=id)
    base  = get_object_or_404(Tbdocumentobase, id=requisicao_viatura.tbdocumentobase.id)
     
    if validacao(request, "edicao"):
        
        # validando campos para uso no formato datetime do atributo datainicio dos servicos
        hrinicio = request.POST['horainicio']
        mininicio = request.POST['mininicio']
        if hrinicio == '':
            hrinicio = str( requisicao_viatura.dtinicioservicos.hour )
        if mininicio == '':
            mininicio = str( requisicao_viatura.dtinicioservicos.minute )
                
        servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        dtsolicitante = datetime.datetime.strptime( request.POST['dtsolicitante'], "%d/%m/%Y")
        dtautorizado = datetime.datetime.strptime( request.POST['dtautorizado'], "%d/%m/%Y")
        dtinicio = datetime.datetime.strptime( request.POST['dtinicio']+" "+hrinicio+":"+mininicio , "%d/%m/%Y %H:%M")
            
        
        # verificando os grupos do usuario
        for obj in servidor:
            if request.POST.get(obj.nmservidor, False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = Tbdocumentoservidor.objects.filter( tbdocumentobase__id = base.id, tbservidor__id = obj.id )
                if not res:
                    # inserir ao authusergroups
                    ug = Tbdocumentoservidor( tbdocumentobase = base,
                                          tbservidor = Tbservidor.objects.get( pk = obj.id ) )
                    ug.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = Tbdocumentoservidor.objects.filter( tbdocumentobase__id = base.id, tbservidor__id = obj.id )
                if res:
                    # excluir do authusergroups
                    for aug in res:
                        aug.delete()
                    #print obj.name + ' desmarcou deste usuario'
        
        # cadastrando o registro processo base            
        f_base = Tbdocumentobase (
                                    id = base.id,
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentovr' ),
                                    dtdocumento = dtsolicitante,
                                    dtcadastrodocumento = base.dtcadastrodocumento,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
        f_base.save()

        f_requisicao_viatura = Tbdocumentovr (
                                       id = requisicao_viatura.id,
                                       objetivo = request.POST['objetivo'],
                                       destino = request.POST['destino'],
                                       tempodias = request.POST['tempodias'],
                                       motorista = request.POST['motorista'],
                                       usuarios = request.POST['usuarios'],
                                       localviatura = request.POST['localviatura'],
                                       dtsolicitante = dtsolicitante,
                                       dtinicioservicos = dtinicio,
                                       dtautorizado = dtautorizado,
                                       veiculo = request.POST['veiculo'],
                                       placa = request.POST['placa'],
                                       tbdocumentobase = f_base,
                                       )
        f_requisicao_viatura.save()
            
        return HttpResponseRedirect("/sicop/restrito/documento/edicao/"+str(base.id)+"/")
    
    
    
    return render_to_response('sicop/restrito/documento/requisicao_viatura/edicao.html',
                              {'base':base,'vr':requisicao_viatura},
                               context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if request_form.POST['nmdocumento'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do documento')
        warning = False
    if request_form.POST['objetivo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o objetivo')
        warning = False
    if request_form.POST['destino'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o destino')
        warning = False
    if request_form.POST['tempodias'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o tempo em dias')
        warning = False
    if request_form.POST['motorista'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o motorista')
        warning = False
    if request_form.POST['usuarios'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe os usuarios')
        warning = False
    if request_form.POST['localviatura'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o local de apresentacao')
        warning = False
    if request_form.POST['dtsolicitante'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a data solicitante')
        warning = False
    if request_form.POST['veiculo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o veiculo')
        warning = False
    if request_form.POST['placa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a placa')
        warning = False

    return warning 

