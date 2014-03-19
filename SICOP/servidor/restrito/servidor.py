from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages

from sicop.forms import FormPecasTecnicas, FormServidor,FormFerias

from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa,Tbcontrato,\
    Tbservidor, AuthUser, Tbdivisao, Tbferias, Tbsituacao, Tbdocumentoservidor
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import datetime
from datetime import timedelta
from sicop.restrito.processo import formatDataToText

nome_relatorio = "relatorio_servidor"
response_consulta = "/ConsultarServidor/"
titulo_relatorio = "Relatorio Servidores"
planilha_relatorio = "Servidores"

    
#SERVIDORES -----------------------------------------------------------------------------------------------------------------------------
@permission_required('servidor.servidor_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        servidor = request.POST['servidor']
        contrato = request.POST['contrato']
        lista = Tbservidor.objects.all().filter( nmservidor__icontains=servidor,nmcontrato__icontains=contrato)
    else:
        lista = Tbservidor.objects.all()
    lista = lista.order_by( 'nmservidor' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_servidor'] = lista
    return render_to_response('controle/servidor/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

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
            return HttpResponseRedirect("/ConsultarServidor/")
    return render_to_response('controle/servidor/cadastro.html',{'divisao':divisao}, context_instance = RequestContext(request))

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
            return HttpResponseRedirect("/EditarServidor/"+str(id)+"/")
    return render_to_response('controle/servidor/edicao.html',
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