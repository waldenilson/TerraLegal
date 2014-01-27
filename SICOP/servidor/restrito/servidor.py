from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages

from sicop.forms import FormPecasTecnicas, FormServidor,FormFerias

from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa,Tbcontrato, Tbservidor, AuthUser, Tbdivisao, Tbferias
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import datetime
from sicop.restrito.processo import formatDataToText

nome_relatorio = "relatorio_servidor"
response_consulta = "/controle/restrito/servidor/consulta/"
titulo_relatorio = "Relatorio Servidores"
planilha_relatorio = "Servidores"

    
#SERVIDORES -----------------------------------------------------------------------------------------------------------------------------
@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        servidor = request.POST['servidor']
        lista = Tbservidor.objects.all().filter( nmservidor__icontains=servidor)
    else:
        lista = Tbservidor.objects.all()
    lista = lista.order_by( 'nmservidor' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_servidor'] = lista
    return render_to_response('controle/servidor/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))


@permission_required('servidor.servidor_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastroferias(request,id): #id se refere ao servidor
    servidor = Tbservidor.objects.filter(id = id)
    ferias = Tbferias.objects.all().filter(tbservidor=id)
    
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
                    dtInicio2 = dtInicio2,
                    nrDias2 = nrDias2,
                    dtInicio3 = dtInicio3,
                    nrDias3 = nrDias3,
                    stAntecipa = stAntecipa,
                    stDecimoTerceiro = stDecimoTerceiro,
                    stSituacao = request.POST['stSituacao'],
                    )
            f_ferias.save()
            #colocar aqui uma chamada para as ferias cadastradas do servido
            return HttpResponseRedirect("/controle/restrito/servidor/consulta/")
    else:
            return render_to_response('controle/servidor/cadastroFerias.html',{'servidor':servidor,'ferias':ferias}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicaoferias(request, id): #esse id se refere as ferias
    ferias = get_object_or_404(Tbferias, id=id)
    servidor = Tbservidor.objects.get(id = Tbferias.objects.get(pk = id).tbservidor_id)

    dtInicio1 = formatDataToText(ferias.dtInicio1)
    dtInicio2 = formatDataToText(ferias.dtInicio2)
    dtInicio3 = formatDataToText(ferias.dtInicio3)
    #print "vem do banco"
    #print dtInicio1
    
    if ferias.nrDias1 == None:
        ferias.nrDias1 = ""
    if ferias.nrDias2 == None:
        ferias.nrDias2 = ""
    if ferias.nrDias3 == None:
        ferias.nrDias3 = ""
        
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
                    dtInicio2 = dtInicio2,
                    nrDias2 = nrDias2,
                    dtInicio3 = dtInicio3,
                    nrDias3 = nrDias3,
                    stAntecipa = stAntecipa,
                    stDecimoTerceiro = stDecimoTerceiro,
                    stSituacao = request.POST['stSituacao'],
                    )
        f_ferias.save()
        return HttpResponseRedirect("/controle/restrito/servidor/edicao/"+str(servidor.id)+"/")
    else:
        return render_to_response('controle/servidor/edicaoFerias.html',{'ferias':ferias,'servidor':servidor,'dtInicio1':dtInicio1,'dtInicio2':dtInicio2,'dtInicio3':dtInicio3},context_instance = RequestContext(request))

@permission_required('servidor.servidor_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    #usar quando tives chaves
    #contrato = Tbcontrato.objects.all()
    #caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    #gleba = Tbgleba.objects.all()
    divisao = Tbdivisao.objects.all()
    if request.method == "POST":
        if validacao(request):
            _nrCPF = request.POST['nrcpf'].replace('.','').replace('-','')
            if not _nrCPF:
                _nrCPF = None
            f_servidor = Tbservidor(
                    nmservidor = request.POST['nmservidor'],
                    nmunidade = request.POST['nmunidade'],
                    nmlotacao = request.POST['nmlotacao'],
                    cdsiape = request.POST['cdsiape'],
                    nrcpf = _nrCPF,
                    dsportariacargo = request.POST['dsportariacargo'],
                    dsportaria = request.POST['dsportaria'],
                    nmcargo = request.POST['nmcargo'],
                    nrtelefone1 = request.POST['nrtelefone1'],
                    nrtelefone2 = request.POST['nrtelefone2'],
                    email = request.POST['email'],
                    dsatividades = request.POST['dsatividades'],
                    tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao']),
                    )
            f_servidor.save()
            return HttpResponseRedirect("/controle/restrito/servidor/consulta/")
    return render_to_response('controle/servidor/cadastro.html',{'divisao':divisao}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    ferias = Tbferias.objects.filter(tbservidor = id)
    instance = get_object_or_404(Tbservidor, id=id)
    if request.method == "POST":
        if validacao(request):
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
                    nrtelefone1 = request.POST['nrtelefone1'],
                    nrtelefone2 = request.POST['nrtelefone2'],
                    email = request.POST['email'],
                    dsatividades = request.POST['dsatividades'],
                    tbdivisao = AuthUser.objects.get(pk = request.user.id ).tbdivisao
                    )
            f_servidor.save()
            return HttpResponseRedirect("/controle/restrito/servidor/edicao/"+str(id)+"/")
    return render_to_response('controle/servidor/edicao.html',
                              {"servidor":instance , "ferias":ferias},context_instance = RequestContext(request))

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
        warning = False
    return warning