from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.forms import FormServidor

from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato, Tbservidor
from sicop.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

nome_relatorio      = "relatorio_servidor"
response_consulta  = "/controle/restrito/servidor/consulta/"
titulo_relatorio    = "Relatorio Servidores"
planilha_relatorio  = "Servidores"

#SERVIDORES -----------------------------------------------------------------------------------------------------------------------------

@login_required
def consulta(request):
    if request.method == "POST":
        #requerente = request.POST['requerente']
        #cpf = request.POST['cpf']
        #entrega = request.POST['entrega']
        servidor = request.POST['servidor']
        #lista = Tbpecastecnicas.objects.all().filter( nmrequerente__contains=requerente, nrcpfrequerente__contains=cpf, nrentrega__contains=entrega )
        lista = Tbservidor.objects.all().filter( nmservidor__icontains=servidor)
    
    else:
        lista = Tbservidor.objects.all()
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_servidor'] = lista
    #return render_to_response('sicop/restrito/peca_tecnica/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    return render_to_response('controle/servidor/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    #usar quando tives chaves 
    #contrato = Tbcontrato.objects.all()
    #caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    #gleba = Tbgleba.objects.all()
    if request.method == "POST":
        form = FormServidor(request.POST)
        if validacao(request):
            if form.is_valid(): # tem que preencher todos campos com os tipos que correspondem
                f = form.save(commit=False)
                f.nrCPF = request.POST['nrcpfrequerente'].replace('.','').replace('-','')
                form.save()
                return HttpResponseRedirect( response_consulta ) 
    else:
        form = FormServidor() #gera registro novo
    
    #return render_to_response('sicop/restrito/peca_tecnica/cadastro.html',{"form":form,'caixa':caixa,'contrato':contrato,'gleba':gleba}, context_instance = RequestContext(request))
    return render_to_response('controle/servidor/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    #usar abaixo se tiver FK tem que recuperar todas antes de exibir
    ##contrato = Tbcontrato.objects.all()
    ##caixa = Tbcaixa.objects.filter( tbtipocaixa = 2 )
    #gleba = Tbgleba.objects.all()
    
    instance = get_object_or_404(Tbservidor, id=id)
        
    if request.method == "POST":
        form = FormServidor(request.POST,request.FILES,instance=instance)
        
        if validacao(request):
            if form.is_valid():
                print 'passou form is valid'
                f = form.save(commit=False)
                print f.nrCPF 
                f.nrCPF = request.POST['nrcpfrequerente'].replace('.','').replace('-','')
                form.save()
                return HttpResponseRedirect("/sicop/restrito/servidor/edicao/"+str(id)+"/")
    else:
        form = FormServidor(instance=instance) 

    return render_to_response('controle/servidor/edicao.html',
                              {"form":form}, 
                              context_instance = RequestContext(request))


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
