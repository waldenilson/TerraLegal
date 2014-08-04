# Create your views here.
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required,login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages


from sicop.models import  AuthUser, Tbdivisao, Tbdocumentoservidor, Tbsituacao
from servidor.models import Tbferias, Tbservidor

from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import datetime
from datetime import timedelta

from sicop.restrito.processo import formatDataToText

import random
import time

nome_relatorio = "relatorio_servidor"
response_consulta = "/servidor/consulta/"
titulo_relatorio = "Relatorio Servidores"
planilha_relatorio = "Servidores"


@login_required
def inicio(request):
    return render(request, "base/acesso_restrito.html")

@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        servidor = request.POST['servidor']
        contrato = request.POST['contrato']
        lista = Tbservidor.objects.all().filter( nmservidor__icontains=servidor,nmcontrato__icontains=contrato)
    else:
        lista = Tbservidor.objects.all()
    lista = lista.order_by( 'nmservidor' )
    '''gravando na sessao o resultado da consulta preparando para o relatorio/pdf'''
    request.session['relatorio_servidor'] = lista
    return render_to_response('consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    divisao = Tbdivisao.objects.all()
    if request.method == "POST":
       
        if validacao(request):
            _nrCPF = request.POST['nrcpf'].replace('.','').replace('-','')
            if not _nrCPF:
                _nrCPF = None
                
            dtnascimento = None
            if request.POST['dtnascimento']:
                dtnascimento = datetime.datetime.strptime( request.POST['dtnascimento'], "%d/%m/%Y")

            f_servidor = Tbservidor(
                    nmservidor = request.POST['nmservidor'],
                    nmunidade = request.POST['nmunidade'],
                    nmlotacao = request.POST['nmlotacao'],
                    cdsiape = request.POST['cdsiape'],
                    nrcpf = request.POST['nrcpf'].replace('.','').replace('-',''),
                    dsportariacargo = request.POST['dsportariacargo'],
                    dsportaria = request.POST['dsportaria'],
                    nmcargo = request.POST['nmcargo'],
                    nrtelefone1 = request.POST['nrtelefone1'].replace('(','').replace(')','').replace('-',''),
                    nrtelefone2 = request.POST['nrtelefone2'].replace('(','').replace(')','').replace('-',''),
                    email = request.POST['email'],
                    dsatividades = request.POST['dsatividades'],
                    tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao']),
                    nmcontrato = request.POST['nmcontrato'],
                    dtnascimento = dtnascimento
                    )
            f_servidor.save()
            return HttpResponseRedirect("/servidor/consulta/")
    return render_to_response('cadastro.html',{'divisao':divisao}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    ferias = Tbferias.objects.filter(tbservidor = id)
    instance = get_object_or_404(Tbservidor, id=id)
    situacaoferias  = Tbsituacao.objects.all().filter(cdTabela="ferias")
    documentos  = Tbdocumentoservidor.objects.filter(tbservidor = id)
    dtnascimento = formatDataToText(instance.dtnascimento)
    
    if request.method == "POST":
        if not request.user.has_perm('servidor.servidor_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 
        if validacao(request):
            dtnascimento = None
            if request.POST['dtnascimento']:
                dtnascimento = datetime.datetime.strptime(request.POST['dtnascimento'], "%d/%m/%Y")
            f_servidor = Tbservidor(
                    id = instance.id,
                    nmservidor = request.POST['nmservidor'],
                    nmunidade = request.POST['nmunidade'],
                    nmlotacao = request.POST['nmlotacao'],
                    cdsiape = request.POST['cdsiape'],
                    nrcpf = request.POST['nrcpf'].replace('.','').replace('-',''),
                    dsportariacargo = request.POST['dsportariacargo'],
                    dsportaria = request.POST['dsportaria'],
                    nmcargo = request.POST['nmcargo'],
                    nrtelefone1 = request.POST['nrtelefone1'].replace('(','').replace(')','').replace('-',''),
                    nrtelefone2 = request.POST['nrtelefone2'].replace('(','').replace(')','').replace('-',''),
                    email = request.POST['email'],
                    dsatividades = request.POST['dsatividades'],
                    tbdivisao = AuthUser.objects.get(pk = request.user.id ).tbdivisao,
                    nmcontrato = request.POST['nmcontrato'],
                    dtnascimento = dtnascimento
                    
                    )
            f_servidor.save()
            return HttpResponseRedirect("/servidor/edicao/"+str(id)+"/")
    return render_to_response('edicao.html',
                              {"servidor":instance , "ferias":ferias, "situacaoferias":situacaoferias ,"documentos":documentos,"dtnascimento":dtnascimento},context_instance = RequestContext(request))

@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','CARGO') )
        for obj in lista:
            dados.append( ( obj.nmservidor , obj.nmcargo ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Cargo' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmservidor)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.nmcargo)
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

@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Cargo'])
        for obj in lista:
            writer.writerow([obj.nmservidor, obj.nmcargo])
        return response
    else:
        return HttpResponseRedirect( response_consulta )

def validacao(request_form):
    warning = True
    if request_form.POST['nmservidor'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe nome do servidor')
    return warning

'''
Modulo de ferias
'''

@permission_required('servidor.servidor_cadastro_ferias', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastroferias(request,id): #id se refere ao servidor
    servidor = Tbservidor.objects.filter(id = id)
    ferias   = Tbferias.objects.all().filter(tbservidor=id)
    situacao = Tbsituacao.objects.all().filter(cdTabela="ferias")
    
    if request.method == "POST":
            stAntecipa = False
            if request.POST.get('stAntecipa',False):
                stAntecipa = True
            stDecimoTerceiro = False
            if request.POST.get('stDecimoTerceiro',False):
                stDecimoTerceiro = True
            
            dtInicio1 = None
            if request.POST['dtInicio1']:
                dtInicio1 = datetime.datetime.strptime( request.POST['dtInicio1'], "%d/%m/%Y")
            dtInicio2 = None
            if request.POST['dtInicio2']:
                dtInicio2 = datetime.datetime.strptime( request.POST['dtInicio2'], "%d/%m/%Y")
            dtInicio3 = None
            if request.POST['dtInicio3']:
                dtInicio3 = datetime.datetime.strptime( request.POST['dtInicio3'], "%d/%m/%Y")
            
            nrDias1 = request.POST['nrDias1']
            if not request.POST['nrDias1']:
                nrDias1 = None
            nrDias2 = request.POST['nrDias2']
            if not request.POST['nrDias2']:
                nrDias2 = None
            nrDias3 = request.POST['nrDias3']
            if not request.POST['nrDias3']:
                nrDias3 = None
                
            f_ferias = Tbferias(
                    tbservidor_id = id,
                    nrAno = request.POST['nrAno'],
                    dtInicio1 = dtInicio1,
                    nrDias1 = nrDias1,
                    stSituacao1 = Tbsituacao.objects.get( pk = request.POST['tbsituacao1'] ),
                    dtInicio2 = dtInicio2,
                    nrDias2 = nrDias2,
                    stSituacao2 = Tbsituacao.objects.get( pk = request.POST['tbsituacao2'] ),
                    dtInicio3 = dtInicio3,
                    nrDias3 = nrDias3,
                    stSituacao3 = Tbsituacao.objects.get( pk = request.POST['tbsituacao3'] ),
                    stAntecipa = stAntecipa,
                    stDecimoTerceiro = stDecimoTerceiro,
                    
                    )
            f_ferias.save()
            #colocar aqui uma chamada para as ferias cadastradas do servido
            return HttpResponseRedirect("/servidor/consulta/")
    else:
            return render_to_response('cadastroFerias.html',{'servidor':servidor,'ferias':ferias,'situacao':situacao}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_edicao_ferias', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicaoferias(request, id): #esse id se refere as ferias
    ferias = get_object_or_404(Tbferias, id=id)
    servidor = Tbservidor.objects.get(id = Tbferias.objects.get(pk = id).tbservidor_id)
    situacao = Tbsituacao.objects.all().filter(cdTabela="ferias")
    
    dtInicio1 = formatDataToText(ferias.dtInicio1)
    dtInicio2 = formatDataToText(ferias.dtInicio2)
    dtInicio3 = formatDataToText(ferias.dtInicio3)
 
    if ferias.nrDias1 == None:
        ferias.nrDias1 = ""
        dtFim1 = ""
    else:
        dtFim1 = formatDataToText(ferias.dtInicio1 + timedelta(ferias.nrDias1 - 1))
        
    
    if ferias.nrDias2 == None:
        ferias.nrDias2 = ""
        dtFim2 = ""
    else:
        dtFim2 = formatDataToText(ferias.dtInicio2 + timedelta(ferias.nrDias2 - 1))
    
    if ferias.nrDias3 == None:
        ferias.nrDias3 = ""
        dtFim3 = ""
    else:
        dtFim3 = formatDataToText(ferias.dtInicio3 + timedelta(ferias.nrDias3 - 1))
        
    if request.method == "POST":
        if validacaoferias(request):
            stAntecipa = False
            if request.POST.get('stAntecipa',False):
                stAntecipa = True
            stDecimoTerceiro = False
            if request.POST.get('stDecimoTerceiro',False):
                stDecimoTerceiro = True
        
            dtInicio1 = None
            if request.POST['dtInicio1']:
                dtInicio1 = datetime.datetime.strptime( request.POST['dtInicio1'], "%d/%m/%Y")
            dtInicio2 = None
            if request.POST['dtInicio2']:
                dtInicio2 = datetime.datetime.strptime( request.POST['dtInicio2'], "%d/%m/%Y")
            dtInicio3 = None
            if request.POST['dtInicio3']:
                dtInicio3 = datetime.datetime.strptime( request.POST['dtInicio3'], "%d/%m/%Y")
                 
            nrDias2 = request.POST['nrDias2']
            if nrDias2 == "":
                nrDias2 = None
       
            nrDias3 = request.POST['nrDias3']
            if nrDias3 == "":
                nrDias3 = None
            f_ferias = Tbferias(
                        id = ferias.id,# se nao colocar essa linha ele cria um novo
                        tbservidor_id = servidor.id,
                        nrAno = request.POST['nrAno'],
                        dtInicio1 = dtInicio1,
                        nrDias1 = request.POST['nrDias1'],
                        stSituacao1 = Tbsituacao.objects.get( pk = request.POST['tbsituacao1']),
                        dtInicio2 = dtInicio2,
                        nrDias2 = nrDias2,
                        stSituacao2 = Tbsituacao.objects.get( pk = request.POST['tbsituacao2']),
                        dtInicio3 = dtInicio3,
                        nrDias3 = nrDias3,
                        stSituacao3 = Tbsituacao.objects.get( pk = request.POST['tbsituacao3']),
                        stAntecipa = stAntecipa,
                        stDecimoTerceiro = stDecimoTerceiro,
                        
                        )
            f_ferias.save()
            return HttpResponseRedirect("/servidor/edicao/"+str(servidor.id)+"/")
    return render_to_response('edicaoFerias.html',{'ferias':ferias,'servidor':servidor,'dtInicio1':dtInicio1,'dtInicio2':dtInicio2,'dtInicio3':dtInicio3,'situacao':situacao,'dtFim1':dtFim1,'dtFim2':dtFim2,'dtFim3':dtFim3},context_instance = RequestContext(request))


def validacaoferias(request_form):
    warning = True
    if request_form.POST['nrDias1'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade de dias do 1o. periodo')
        warning = False
    return warning

def demo_linewithfocuschart(request):
    """
    linewithfocuschart page
    """
    nb_element = 100
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)

    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)
    ydata3 = map(lambda x: x * 3, ydata)
    ydata4 = map(lambda x: x * 4, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                   "date_format": tooltip_date}
    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
        'name3': 'series 3', 'y3': ydata3, 'extra3': extra_serie,
        'name4': 'series 4', 'y4': ydata4, 'extra4': extra_serie
    }
    charttype = "lineWithFocusChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('controle/servidor/linewithfocuschart.html', data)
