from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context
from TerraLegal.tramitacao.models import Tbcaixa, Tbtipocaixa, AuthUser, Tbprocessobase,\
    Tbpecastecnicas, Tbprocessorural, Tbprocessosanexos, Tbprocessoclausula, Tbprocessourbano, Tbdivisao,\
    Tbetapa, Tbtipoprocesso, Tbchecklist, Tbchecklistprocessobase,\
    Tbetapaanterior, Tbetapaposterior, Tbtransicao, Tbprocessobaseetapa
from django.http import HttpResponseRedirect
from django.contrib import messages
from TerraLegal.tramitacao.forms import FormCaixa
from TerraLegal.tramitacao.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
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
from django.db.models import Q
import datetime

nome_relatorio = "relatorio_etapa"
response_consulta = "/sicop/etapa/consulta/"
titulo_relatorio = "Relatorio Etapas"
planilha_relatorio = "Etapas"

@permission_required('sicop.etapa_checklist_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def restaurar(request, processo):
    #excluir o ultimo registro de  tbtransicao
    tran = Tbtransicao.objects.filter( tbprocessobase = processo ).order_by( '-dttransicao' )
    if len(tran) > 1:
        tran[0].delete()
        print 'etapa: '+tran[1].tbetapa.nmfase
        proc = Tbprocessobase.objects.get( pk = processo )
        proc.tbetapaatual = tran[1].tbetapa
        proc.save()
    return HttpResponseRedirect("/sicop/processo/edicao/"+str(processo)+"/")
    

@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmfase']
        lista = Tbetapa.objects.filter( 
            nmfase__icontains=nome, 
            tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        #lista = Tbetapa.objects.filter( nmfase__icontains=nome )
    else:
        lista = Tbetapa.objects.filter( 
            tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        #lista = Tbetapa.objects.all()
        
    lista = lista.order_by( 'tbtipoprocesso__nome','ordem', 'nmfase' )
    
#gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session[nome_relatorio] = lista
    return render_to_response('sicop/etapa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.etapa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('id')
       
    if request.method == "POST":


        inicial = False
        if request.POST.get('blinicial',False):
            inicial = True

        next = request.GET.get('next', '/')
        if validacao(request, False):
            f_fase = Tbetapa(
                              nmfase = request.POST['nmfase'],
                              titulo = request.POST['titulo'],
                              tbtipoprocesso = Tbtipoprocesso.objects.get(pk = request.POST['tbtipoprocesso']),
                              dsfase = request.POST['dsfase'],
                              ordem = request.POST['ordem'],
                              blativo = True,
                              blinicial = inicial,
                              tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                              )
            f_fase.save()
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:
                return HttpResponseRedirect(next)
    return render_to_response('sicop/etapa/cadastro.html',{"tipoprocesso":tipoprocesso}, context_instance = RequestContext(request))


@permission_required('sicop.etapa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Tbetapa, id=id)
    tipoprocesso = Tbtipoprocesso.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('id')

    etapas = Tbetapa.objects.exclude( id = instance.id ).order_by('id')
    etapas = etapas.filter( tbtipoprocesso__id = instance.tbtipoprocesso.id )
    etapasAnteriores = Tbetapaanterior.objects.filter( tbetapa__id = instance.id ).order_by('id')
    etapasPosteriores = Tbetapaposterior.objects.filter( tbetapa__id = instance.id ).order_by('id')
    checklists = Tbchecklist.objects.filter( tbetapa__id = instance.id ).order_by('id')
    
    ativo = False
    if request.POST.get('blativo',False):
        ativo = True
    
    inicial = False
    if request.POST.get('blinicial',False):
        inicial = True

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
    
    etapadesejada = None
    for et in etapasPosteriores:
        if et.blsequencia:
            etapadesejada = et
            break

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
                if request.POST['etapadesejada'] == str(pos.tbposterior.id):
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
                              titulo = request.POST['titulo'],
                              tbtipoprocesso = Tbtipoprocesso.objects.get(pk = request.POST['tbtipoprocesso']),
                              dsfase = request.POST['dsfase'],
                              ordem = request.POST['ordem'],
                              blativo = ativo,
                              blinicial = inicial,
                              tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                            )
            f_fase.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/etapa/edicao/"+str(id)+"/")
            else:
                return HttpResponseRedirect(next)
    return render_to_response('sicop/etapa/edicao.html',
        {"fase":instance,'etapas':etapas,"tipoprocesso":tipoprocesso,'checklists':checklists,
        'anteriores':anteriores,'posteriores':posteriores,'etapadesejada':etapadesejada}, context_instance = RequestContext(request))


@permission_required('sicop.processo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def checklist(request, processo, etapa):
    obj_processo = Tbprocessobase.objects.get( pk = processo )
    obj_etapa = Tbetapa.objects.get( pk = etapa )
    processoetapa = Tbprocessobaseetapa.objects.filter(tbprocessobase__id = obj_processo.id, tbetapa__id = obj_etapa.id)
    dsparecer = ''
    if processoetapa:
        dsparecer = processoetapa[0].dsparecer

    checklist = Tbchecklist.objects.filter( tbetapa__id = etapa ).order_by('nmchecklist')
    procChecklist = Tbchecklistprocessobase.objects.filter( tbprocessobase__id = processo )
    posteriores = Tbetapaposterior.objects.filter( tbetapa__id = etapa )

    result = {}
    for obj in checklist:
        achou = False
        for obj2 in procChecklist:
            if obj.id == obj2.tbchecklist.id:
                result.setdefault(obj, obj2)
                achou = True
                break
        if not achou:
            result.setdefault(obj, False)
    result = sorted(result.items())
    
    # buscar os checklists pendentes das etapas das transacoes anteriores
    checkpendentes = []
    transicao = Tbtransicao.objects.filter( tbprocessobase__id = obj_processo.id ).order_by('-dttransicao')
    
    x = 0
    for tran in transicao:
      if x!=0:
        checks = Tbchecklist.objects.filter( tbetapa__id = tran.tbetapa.id )
        for c in checks:
            obj = Tbchecklistprocessobase.objects.filter( tbchecklist__id = c.id, tbprocessobase__id = obj_processo.id )
            if obj:
                if obj[0].blnao_obrigatorio == False and obj[0].blsanado == False :
                    checkpendentes.append( c )
            else:
                checkpendentes.append( c )
      x += 1


    if request.method == "POST":
    
        processoetapa = Tbprocessobaseetapa.objects.filter(tbprocessobase__id = obj_processo.id, tbetapa__id = obj_etapa.id)
        if processoetapa:
            processoetapa[0].dsparecer = request.POST['dsparecer']
            processoetapa[0].save()
        else:
            objpe = Tbprocessobaseetapa(
                    tbprocessobase = obj_processo,
                    tbetapa = obj_etapa,
                    dsparecer = request.POST['dsparecer']
                )
            objpe.save()

        if request.POST.get('atual',False):
            
            transicao = Tbtransicao(
                tbprocessobase = obj_processo,
                tbetapa = obj_etapa,
                dttransicao = datetime.datetime.now(),
                auth_user = AuthUser.objects.get( pk = request.user.id ),
            )

            t = Tbtransicao.objects.all().order_by('-id')
            if t:
                if t[0].tbetapa.id != obj_etapa.id or t[0].tbprocessobase.id != obj_processo.id:
                    transicao.save()
            else:
                transicao.save()

            proc = obj_processo
            proc.tbetapaatual = transicao.tbetapa
            proc.save()

            return HttpResponseRedirect("/sicop/processo/edicao/"+str(processo))
        else:
            if request.POST['etapaposterior'] != '':
                transicao = Tbtransicao(
                             tbprocessobase = Tbprocessobase.objects.get( pk = processo ) ,
                             tbetapa = Tbetapa.objects.get( pk = request.POST['etapaposterior'] ),
                             dttransicao = datetime.datetime.now(),
                             auth_user = AuthUser.objects.get( pk = request.user.id ),
                            )

                # se etapa atual nao for a propria em questao, registra a transicao
                t = Tbtransicao.objects.all().order_by('-id')
                if t:
                    if t[0].tbetapa.id != transicao.tbetapa.id or t[0].tbprocessobase.id != transicao.tbprocessobase.id:
                        if t[0].tbetapa.id != transicao.tbetapa.id:
                            transicao.save()
                            # altera a etapa atual no processobase
                            proc = Tbprocessobase.objects.get( pk = processo )
                            proc.tbetapaatual = Tbetapa.objects.get( pk = request.POST['etapaposterior'] )
                            proc.save()
    
        
        if not request.user.has_perm('sicop.etapa_checklist_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/')







        checked = 0
        # percorre a lista dos checks da etapa
        for obj in checklist:
                
            blnao_obrigatorio = False
            if request.POST.get(str(obj.id), False):
                blnao_obrigatorio = True
                #print 'BL NAO OBRIGATORIO: '+obj.nmchecklist


            nmcustom = ''
            dtcustom = None
            blemprogramacao = False

            if obj.blcustomtext or obj.blcustomdate:
                blemprogramacao = request.POST.get(str(obj.id)+'-emprogramacao', False)
                if request.POST.get(str(obj.id)+'-nmcustom', False):
                    nmcustom = request.POST[str(obj.id)+'-nmcustom']
                if request.POST.get(str(obj.id)+'-dtcustom', False):
                    try:
                        dtcustom = datetime.datetime.strptime( request.POST[str(obj.id)+'-dtcustom'], "%d/%m/%Y")
                    except:
                        dtcustom = None

            res = Tbchecklistprocessobase.objects.filter( tbprocessobase__id = processo, tbchecklist__id = obj.id )
            # se o check veio marcado ou com campo extra preenchido
            if request.POST.get(obj.nmchecklist, False) or nmcustom != '' or dtcustom != None:
                checked += 1

                #verifica se esse check ja esta ligado ao processo
                if res:
                    cp = res[0]
                    cp.blnao_obrigatorio = blnao_obrigatorio
                    if request.POST.get(obj.nmchecklist, False):
                        cp.blsanado = True
                    else:
                        cp.blsanado = False
                    cp.nmcustom = nmcustom
                    cp.dtcustom = dtcustom
                    cp.bl_em_programacao = blemprogramacao
                    cp.save()
                else:
                    # inserir ao checkprocesso
                    cp = Tbchecklistprocessobase( tbprocessobase = Tbprocessobase.objects.get( pk = processo ),
                                          tbchecklist = Tbchecklist.objects.get( pk = obj.id ), blnao_obrigatorio = blnao_obrigatorio, nmcustom = nmcustom, dtcustom = dtcustom )
                    if request.POST.get(obj.nmchecklist, False):
                        cp.blsanado = True
                    else:
                        cp.blsanado = False
                    cp.nmcustom = nmcustom
                    cp.dtcustom = dtcustom
                    cp.bl_em_programacao = blemprogramacao
                    cp.save()

            # se o check veio desmarcado
            else:
                # se o check tiver um registro ligado ao processo
                if res:
                    for cp in res:
                        cp.blnao_obrigatorio = blnao_obrigatorio
                        cp.blsanado = False
                        cp.nmcustom = nmcustom
                        cp.dtcustom = dtcustom
                        cp.bl_em_programacao = blemprogramacao
                        cp.save()
                elif blnao_obrigatorio:
                    cp = Tbchecklistprocessobase( tbprocessobase = Tbprocessobase.objects.get( pk = processo ),
                                          tbchecklist = Tbchecklist.objects.get( pk = obj.id ), blnao_obrigatorio = blnao_obrigatorio, nmcustom = nmcustom, dtcustom = dtcustom )
                    cp.blsanado = False
                    cp.save()














        
        # se todos os checklists foram marcados

#        if checked == len(checklist):
#            etapas_posterior = Tbetapaposterior.objects.all().filter( tbetapa_id = etapa )
#            etapa_posterior = None
#            if len(etapas_posterior) == 1:
#                etapa_posterior = etapas_posterior[0]
#            else:
#                for et in etapas_posterior:
#                    if et.blsequencia:
#                        etapa_posterior = et
#                        break

#            transicao = Tbtransicao(
#                         tbprocessobase = Tbprocessobase.objects.get( pk = processo ) ,
#                         tbetapa = etapa_posterior.tbposterior,
#                         dttransicao = datetime.datetime.now(),
#                         auth_user = AuthUser.objects.get( pk = request.user.id ),
#                        )

            # se etapa atual nao for a propria em questao, registra a transicao
#            t = Tbtransicao.objects.all().order_by('-id')
#            if t:
#                if t[0].tbetapa.id != transicao.tbetapa.id or t[0].tbprocessobase.id != transicao.tbprocessobase.id:
#                    if t[0].tbetapa.id != transicao.tbetapa.id:
#                        transicao.save()
            
        # se o usuario selecionou alguma etapa posterior para forcar a sequencia do processo
#        else:

        return HttpResponseRedirect("/sicop/processo/edicao/"+str(processo))

    return render_to_response('sicop/etapa/checklist.html',{"checkpendentes":checkpendentes,"processo":obj_processo,"etapa":obj_etapa,'result':result,'posteriores':posteriores,'dsparecer':dsparecer}, context_instance = RequestContext(request))

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
# nome = request_form.POST['nmfase']
# pos = request_form.POST['ordem']
    tipoprocesso = request_form.POST['tbtipoprocesso']
    if edicao:
        seqdesejada = request_form.POST['etapadesejada']
    
    if tipoprocesso == '':
        messages.add_message(request_form,messages.WARNING,'Informe um tipo de processo')
        warning = False

    if edicao:
        # verifica se a ordem desta etapa a ultima. se sim, nao necessita informar uma proxima etapa.
        ordem = request_form.POST['ordem']
        tem_etapa_posterior = False
        result = Tbetapa.objects.order_by('-ordem')
        for r in result:
            tem_etapa_posterior = False
            if int(ordem) < r.ordem:
                tem_etapa_posterior = True
                break
        
        if tem_etapa_posterior:
            if seqdesejada == '':
                messages.add_message(request_form,messages.WARNING,'Informe a Proxima etapa na sequencia desejada')
                warning = False

    return warning