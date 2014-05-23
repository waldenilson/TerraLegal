from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from sicop.models import Tbcaixa, Tbtipocaixa, AuthUser, Tbprocessobase,\
    Tbpecastecnicas, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano, Tbdivisao,\
    Tbetapa, Tbtipoprocesso, Tbchecklist, Tbchecklistprocessobase,\
    Tbetapaanterior, Tbetapaposterior
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.forms import FormCaixa
from sicop.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from odslib import ODS
import csv
from reportlab.platypus.tables import Table
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib import styles
from reportlab.lib.units import cm
import webodt
from webodt import converters, ODFDocument
from webodt.converters import converter
from TerraLegal import settings
from django import conf
import os
from django.template.defaultfilters import join
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import File
import django
from django.core.files import storage
from django.db.models import  Q

nome_relatorio      = "relatorio_etapa"
response_consulta  = "/sicop/restrito/etapa/consulta/"
titulo_relatorio    = "Relatorio Etapas"
planilha_relatorio  = "Etapas"

@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmfase']
        #lista = Tbcaixa.objects.all().filter( nmlocalarquivo__icontains=nome, tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbetapa.objects.filter( nmfase__icontains=nome )
    else:
        #lista = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        lista = Tbetapa.objects.all()
        
    lista = lista.order_by( 'nmfase' )
    
#gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session[nome_relatorio] = lista
    return render_to_response('sicop/restrito/etapa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.etapa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('id')
       
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request, False):
            f_fase = Tbetapa(
                              nmfase = request.POST['nmfase'],
                              tbtipoprocesso = Tbtipoprocesso.objects.get(pk = request.POST['tbtipoprocesso']),
                              dsfase = request.POST['dsfase'],
                              ordem = request.POST['ordem'],
                              blativo = True
                              )
            f_fase.save()
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/restrito/etapa/cadastro.html',{"tipoprocesso":tipoprocesso}, context_instance = RequestContext(request))


@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbetapa, id=id)
    tipoprocesso = Tbtipoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('id')

    etapas = Tbetapa.objects.exclude( id = instance.id ).order_by('id')
    etapasAnteriores = Tbetapaanterior.objects.all().filter( tbetapa__id = instance.id ).order_by('id')
    etapasPosteriores = Tbetapaposterior.objects.all().filter( tbetapa__id = instance.id ).order_by('id')
    
    
    ativo = False
    if request.POST.get('blativo',False):
        ativo = True
        
    #montando anteriores e posteriores
    anteriores = {}
    for obj in etapas:
        achou = False
        for obj2 in etapasAnteriores:
            if obj.id == obj2.tbanterior.id:
                anteriores.setdefault(obj, True)
                achou = True
                break
        if not achou:
            anteriores.setdefault(obj, False)
    anteriores = sorted(anteriores.items())

    posteriores = {}
    for obj in etapas:
        achou = False
        for obj2 in etapasPosteriores:
            if obj.id == obj2.tbposterior.id:
                posteriores.setdefault(obj, True)
                achou = True
                break
        if not achou:
            posteriores.setdefault(obj, False)
    posteriores = sorted(posteriores.items())
    
        

    if request.method == "POST":
        
        if not request.user.has_perm('sicop.etapa_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        # verificando as etapas anteriores
        for obj in etapas:
            if request.POST.get(str(obj.id)+'-anterior', False):
                print obj
                #verificar se esse grupo ja esta ligado ao usuario
                res = Tbetapaanterior.objects.filter( tbanterior__id = obj.id, tbetapa__id = instance.id )
                if not res:
                    # inserir ao authusergroups
                    et = Tbetapaanterior( tbetapa = Tbetapa.objects.get( pk = instance.id ),
                                          tbanterior = Tbetapa.objects.get( pk = obj.id ) )
                    et.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = Tbetapaanterior.objects.filter( tbanterior__id = obj.id, tbetapa__id = instance.id )
                if res:
                    # excluir do authusergroups
                    for et in res:
                        et.delete()

        # verificando as etapas posteriores
        for obj in etapas:
            if request.POST.get(str(obj.id)+'-posterior', False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = Tbetapaposterior.objects.filter( tbposterior__id = obj.id, tbetapa__id = instance.id )
                if not res:
                    # inserir ao authusergroups
                    et = Tbetapaposterior( tbetapa = Tbetapa.objects.get( pk = instance.id ),
                                          tbposterior = Tbetapa.objects.get( pk = obj.id ), blsequencia = False )
                    et.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = Tbetapaposterior.objects.filter( tbposterior__id = obj.id, tbetapa__id = instance.id )
                if res:
                    # excluir do authusergroups
                    for et in res:
                        et.delete()
        
        next = request.GET.get('next', '/')
        if validacao(request, True):
            
            #atribuir false posteriores
            posteriores = Tbetapaposterior.objects.all().filter( tbetapa__id = instance.id ).order_by('id')
            for pos in posteriores:
                if request.POST['etapadesejada'] == pos.tbposterior:
                    posterior = Tbetapaposterior(
                                                 id = pos.id,
                                                 tbetapa = pos.tbetapa,
                                                 tbposterior = pos.tbposterior,
                                                 blsequencia = True
                                                 )
                    posterior.save()
                    
                else:
                    posterior = Tbetapaposterior(
                                                 id = pos.id,
                                                 tbetapa = pos.tbetapa,
                                                 tbposterior = pos.tbposterior,
                                                 blsequencia = False
                                                 )
                    posterior.save()
            
            f_fase = Tbetapa(
                              id = instance.id,
                              nmfase = request.POST['nmfase'],
                              tbtipoprocesso = Tbtipoprocesso.objects.get(pk = request.POST['tbtipoprocesso']),
                              dsfase = request.POST['dsfase'],
                              ordem = request.POST['ordem'],
                              blativo = ativo
                              )
            f_fase.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/etapa/edicao/"+str(id)+"/")
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/restrito/etapa/edicao.html',{"fase":instance,'etapas':etapas,"tipoprocesso":tipoprocesso,'anteriores':anteriores,'posteriores':posteriores}, context_instance = RequestContext(request))


@permission_required('sicop.etapa_checklist', login_url='/excecoes/permissao_negada/', raise_exception=True)
def checklist(request, processo,etapa):    
    obj_processo = Tbprocessobase.objects.get( pk = processo )
    obj_etapa = Tbetapa.objects.get( pk = etapa )
    
    checklist = Tbchecklist.objects.filter( tbfase__id = etapa ).order_by('nmchecklist')
    procChecklist = Tbchecklistprocessobase.objects.filter( tbprocessobase__id = processo )

    result = {}
    for obj in checklist:
        achou = False
        for obj2 in procChecklist:
            if obj.id == obj2.tbchecklist.id:
                result.setdefault(obj.nmchecklist,True)
                achou = True
                break
        if not achou:
            result.setdefault(obj.nmchecklist, False)
    result = sorted(result.items())

    
    return render_to_response('sicop/restrito/etapa/checklist.html',{"processo":obj_processo,"etapa":obj_etapa,'result':result}, context_instance = RequestContext(request))

@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','CAIXA') )
        for obj in lista:
            dados.append( ( obj.nmlocalarquivo , obj.tbtipocaixa.nmtipocaixa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbtipocaixa.nmtipocaixa)    
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([obj.nmlocalarquivo, obj.tbtipocaixa.nmtipocaixa])
        return response
    else:
        return HttpResponseRedirect( response_consulta )


def validacao(request_form, edicao):
    warning = True
#    nome = request_form.POST['nmfase']
#    pos = request_form.POST['ordem']
    tipoprocesso = request_form.POST['tbtipoprocesso']
    if edicao:
        seqdesejada = request_form.POST['etapadesejada']
    
    if tipoprocesso == '':
        messages.add_message(request_form,messages.WARNING,'Informe um tipo de processo')
        warning = False

    if edicao:
        if seqdesejada == '':
            messages.add_message(request_form,messages.WARNING,'Informe a Proxima etapa na sequencia desejada')
            warning = False
#    else:
#        list = []
        # ordem com tipoprocesso eh unico
#        list = Tbfase.objects.filter( ordem= int(pos), tbtipoprocesso__id = tipoprocesso  )
#        if list:
#            messages.add_message(request_form,messages.WARNING,'Numero da ordem usado por outra fase desse tipo de processo')
#            warning = False
#        list = []
        # nome com tipoprocesso eh unico
#        list = Tbfase.objects.filter( nmfase__icontains = nome, tbtipoprocesso__id = tipoprocesso  )
#        if list:
#            messages.add_message(request_form,messages.WARNING,'Informe outro nome da fase')
#            warning = False
    
    return warning