from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia, Tbpregao,\
    Tbdocumentomemorando, Tbdocumentobase, Tbtipodocumento
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from sicop.restrito import processo_rural
from sicop.relatorio_base import relatorio_base, relatorio_documento_base,\
    relatorio_pdf_base_consulta, relatorio_csv_base_consulta,\
    relatorio_ods_base_consulta
from types import InstanceType
from sicop.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson

@login_required
def consulta(request):
    # carrega os processos da divisao do usuario logado
    lista = []
    #lista = Tbprocessobase.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by( "dtcadastrosistema" )
    if request.method == "POST":
        nome = request.POST['nome']
        
        if len(nome) >= 3:
#            lista = Tbprocessobase.objects.all().filter( nrprocesso__contains = numero )
            p_memorando = Tbdocumentomemorando.objects.all().filter( tbdocumentobase__nmdocumento__icontains = nome )
            p_memorando_assunto = Tbdocumentomemorando.objects.all().filter( nmassunto__icontains = nome )
            p_memorando_mensagem = Tbdocumentomemorando.objects.all().filter( nmmensagem__icontains = nome )
            lista = []
            for obj in p_memorando:
                lista.append( obj )
            for obj in p_memorando_assunto:
                lista.append( obj )
            for obj in p_memorando_mensagem:
                lista.append( obj )
        else:
            if len(nome) > 0 and len(nome) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Nome.')
        
    # gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_documento'] = lista
    # gravando na sessao a divisao do usuario logado
    request.session['divisao'] = AuthUser.objects.get( pk = request.user.id ).tbdivisao.nmdivisao +" - "+AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.nmuf
        
    return render_to_response('sicop/restrito/documento/consulta.html',{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Cadastro'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    base = get_object_or_404(Tbdocumentobase, id=id)
    
    tipo = base.tbtipodocumento.tabela
    
    # se processobase pertencer a mesma divisao do usuario logado
    if base.auth_user.tbdivisao.id == AuthUser.objects.get( pk = request.user.id ).tbdivisao.id:
        if tipo == "tbdocumentomemorando":
            memorando = Tbdocumentomemorando.objects.get( tbdocumentobase = id )
                
            return render_to_response('sicop/restrito/documento/memorando/edicao.html',
                                      {'base':base,'memorando':memorando}, context_instance = RequestContext(request))
        
    return HttpResponseRedirect("/sicop/restrito/documento/consulta/")
    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador','Cadastro'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.all()
    escolha = "tbdocumentomemorando"
    div_documento = "memorando"
           
    if request.method == "POST":
        escolha = request.POST['escolha']
        if escolha == "tbdocumentomemorando":
            div_documento = "memorando"
            return render_to_response('sicop/restrito/documento/cadastro.html',
                    {'tipodocumento':tipodocumento,'documento':escolha,
                    'div_documento':div_documento},
                    context_instance = RequestContext(request));  
        
    return render_to_response('sicop/restrito/documento/cadastro.html',{
        'tipodocumento':tipodocumento,'documento':escolha,'div_documento':div_documento}, context_instance = RequestContext(request))

def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_documento']
    if lista:
        resp = relatorio_pdf_base_consulta(request, lista, 'RELATORIO DOS DOCUMENTOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/documento/consulta/")

def relatorio_ods(request):
    return relatorio_ods_base_consulta(request, 
                                       request.session['relatorio_documento'], 
                                       'RELATORIO DOS DOCUMENTOS',
                                       '/sicop/restrito/documento/consulta/')

def relatorio_csv(request):
    return relatorio_csv_base_consulta(request, 
                                       request.session['relatorio_documento'], 
                                       'RELATORIO DOS DOCUMENTOS',
                                       '/sicop/restrito/documento/consulta/')
    
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


