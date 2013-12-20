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
    relatorio_base_consulta
from types import InstanceType
from sicop.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
import xlwt

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

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_documento']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS DOCUMENTOS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/documento/consulta/")

def relatorio_excel(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')  
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    # write the header
    header = ['Header 1', 'Header 2', 'Header 3', 'Header 4']
    for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
           sheet.write(0, hcol, hcol_data, style=xlwt.Style.default_style)
 
    # write your data, you can also get it from your model
    data = ['genius', 'super', 'gorgeous', 'awesomeness']
    for row, row_data in enumerate(data, start=1): # start from row no.1
           for col, col_data in enumerate(row_data):
                 sheet.write(row, col, col_data, style=xlwt.Style.default_style)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=my_data.xls'
    book.save(response)
    return response
    
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


