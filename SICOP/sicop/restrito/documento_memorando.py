
# -*- coding: UTF-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbtipodocumento, Tbdocumentobase,\
    Tbdocumentomemorando, Tbservidor, Tbdocumentoservidor
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

@permission_required('servidor.documento_memorando_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/documento/memorando/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('servidor.documento_memorando_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    div_documento = "memorando"
    escolha = "tbdocumentomemorando"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):

            servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            dtdocumento = datetime.datetime.strptime( request.POST['dtdocumento'], "%d/%m/%Y")
            
            circular = False
            if request.POST.get('blcircular',False):
                circular = True
    
            # cadastrando o registro processo base            
            f_base = Tbdocumentobase (
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentomemorando' ),
                                    dtdocumento = dtdocumento,
                                    dtcadastrodocumento = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()
            
            f_memorando = Tbdocumentomemorando (
                                       nmassunto = request.POST['nmassunto'],
                                       nrsisdoc = request.POST['nrsisdoc'],
                                       nrsufixosisdoc = request.POST['nrsufixosisdoc'],
                                       nmlocal = request.POST['nmlocal'],
                                       nmremetente = request.POST['nmremetente'],
                                       nmdestinatario = request.POST['nmdestinatario'],
                                       nmmensagem = request.POST['nmmensagem'],
                                       blcircular = circular,
                                       tbdocumentobase = f_base,
                                       )
            f_memorando.save()

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

@permission_required('servidor.documento_memorando_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criacao(request, id):   
        
    obj = get_object_or_404(Tbdocumentomemorando, id=id)
    print obj
    ano_sisdoc = obj.tbdocumentobase.dtcadastrodocumento.year
    obj_dia = obj.tbdocumentobase.dtdocumento.day
    obj_mes = mes_do_ano_texto( obj.tbdocumentobase.dtdocumento.month )
    obj_ano = obj.tbdocumentobase.dtdocumento.year
    
    return shortcuts.render_to_response('memorando.odt',dictionary=dict( memorando = obj, anosisdoc = ano_sisdoc, dia = obj_dia, mes = obj_mes, ano = obj_ano ),format='odt',filename=str(obj.tbdocumentobase.nmdocumento)+'.odt')
            
@permission_required('servidor.documento_memorando_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
        
    memorando = get_object_or_404(Tbdocumentomemorando, id=id)
    base  = get_object_or_404(Tbdocumentobase, id=memorando.tbdocumentobase.id)
     
    if validacao(request, "edicao"):
            
        servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        dtdocumento = datetime.datetime.strptime( request.POST['dtdocumento'], "%d/%m/%Y")
        
        circular = False
        if request.POST.get('blcircular',False):
            circular = True

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
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentomemorando' ),
                                    dtdocumento = dtdocumento,
                                    dtcadastrodocumento = base.dtcadastrodocumento,
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
        f_base.save()

        f_memorando = Tbdocumentomemorando (
                                       id = memorando.id,
                                       nmassunto = request.POST['nmassunto'],
                                       nrsisdoc = request.POST['nrsisdoc'],
                                       nrsufixosisdoc = request.POST['nrsufixosisdoc'],
                                       nmlocal = request.POST['nmlocal'],
                                       nmremetente = request.POST['nmremetente'],
                                       nmdestinatario = request.POST['nmdestinatario'],
                                       nmmensagem = request.POST['nmmensagem'],
                                       blcircular = circular,
                                       tbdocumentobase = f_base,
                                       )
        f_memorando.save()
            
        return HttpResponseRedirect("/sicop/restrito/documento/edicao/"+str(base.id)+"/")
    
    return render_to_response('sicop/restrito/documento/memorando/edicao.html',
                              {'base':base,'memorando':memorando},
                               context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if request_form.POST['nmdocumento'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do documento')
        warning = False
    
    return warning 

