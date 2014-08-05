
# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbtipodocumento, Tbdocumentobase,\
    Tbdocumentomemorando, Tbservidor, Tbdocumentoservidor, Tbdocumentorme,\
    Tbdocumentomaterialrme
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

@permission_required('servidor.documento_rme_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/documento/rme/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('servidor.documento_rme_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    div_documento = "rme"
    escolha = "tbdocumentorme"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):

            servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            dtdocumento = datetime.datetime.strptime( request.POST['dtdocumento'], "%d/%m/%Y")
            dtperiodo = datetime.datetime.strptime( request.POST['dtperiodo'], "%d/%m/%Y")
    
            # cadastrando o registro processo base            
            f_base = Tbdocumentobase (
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentorme' ),
                                    dtdocumento = dtdocumento,
                                    dtcadastrodocumento = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()
            
            f_rme = Tbdocumentorme (
                                       dtperiodo = dtperiodo,
                                       nrordem = request.POST['nrordem'],
                                       solicitante = request.POST['solicitante'],
                                       tbdocumentobase = f_base,
                                    )
            f_rme.save()

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

@permission_required('servidor.documento_rme_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criacao(request, id):   
        
    obj = get_object_or_404(Tbdocumentorme, id=id)
    dataperiodo = formatDataToText(obj.dtperiodo)
    data = formatDataToText(obj.tbdocumentobase.dtdocumento)
    
    return shortcuts.render_to_response('rme.odt',dictionary=dict( rme = obj, data = data, dataperiodo = dataperiodo ),format='odt',filename=str(obj.tbdocumentobase.nmdocumento)+'.odt')
            
@permission_required('servidor.documento_rme_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
        
    rme = get_object_or_404(Tbdocumentorme, id=id)
    base  = get_object_or_404(Tbdocumentobase, id=rme.tbdocumentobase.id)
    dtperiodo = formatDataToText(rme.dtperiodo)
    material = Tbdocumentomaterialrme.objects.filter( tbdocumentorme = rme.id ).order_by('especificacao')
     
    if validacao(request, "edicao"):
            
        servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        dtdocumento = datetime.datetime.strptime( request.POST['dtdocumento'], "%d/%m/%Y")
        dtperiodo = datetime.datetime.strptime( request.POST['dtperiodo'], "%d/%m/%Y")
        
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
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentorme' ),
                                    dtdocumento = dtdocumento,
                                    dtcadastrodocumento = base.dtcadastrodocumento,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
        f_base.save()

        f_rme = Tbdocumentorme (
                                       id = rme.id,
                                       dtperiodo = dtperiodo,
                                       nrordem = request.POST['nrordem'],
                                       solicitante = request.POST['solicitante'],
                                       tbdocumentobase = f_base,
                                       )
        f_rme.save()
            
        return HttpResponseRedirect("/sicop/restrito/documento/edicao/"+str(base.id)+"/")
    
    return render_to_response('sicop/restrito/documento/rme/edicao.html',
                              {'base':base,'rme':rme,'material':material,'dtperiodo':dtperiodo},
                               context_instance = RequestContext(request))   


@permission_required('servidor.documento_rme_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criar_material(request, doc):
    rme = get_object_or_404(Tbdocumentorme, id=doc )
    if request.method == "POST":
        if validacaoMaterial(request):
            
            f_material = Tbdocumentomaterialrme(
                                       tbdocumentorme = rme,
                                       especificacao = request.POST['especificacao'],
                                       unidade = request.POST['unidade'],
                                       qtdsolicitada = request.POST['qtdsolicitada']
                                    )
            f_material.save()
                    
            return HttpResponseRedirect("/sicop/restrito/documento/rme/edicao/"+str(rme.id)+"/")
        
    dtperiodo = formatDataToText(rme.dtperiodo)
    return render_to_response('sicop/restrito/documento/rme/edicao.html',
                              {'base':rme.tbdocumentobase,'rme':rme, 'dtperiodo':dtperiodo},
                               context_instance = RequestContext(request))   


def validacaoMaterial(request_form):
    warning = True
    if request_form.POST['especificacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a especificacao.')
        warning = False
    if request_form.POST['unidade'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a unidade.')
        warning = False
    if request_form.POST['qtdsolicitada'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade solicitada.')
        warning = False
    return warning

def validacao(request_form, metodo):
    
    warning = True
    if request_form.POST['solicitante'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o solicitante')
        warning = False
    if request_form.POST['dtdocumento'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a data solicitante')
        warning = False
    if request_form.POST['dtperiodo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a data do periodo')
        warning = False
    if request_form.POST['nrordem'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Nº ordem')
        warning = False

    return warning 

