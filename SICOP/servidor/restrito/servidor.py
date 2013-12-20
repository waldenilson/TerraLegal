from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.forms import FormServidor

from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato, Tbservidor
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo, relatorio_base_excel
import xlwt
from django.http.response import HttpResponse

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
                return HttpResponseRedirect("/controle/restrito/servidor/consulta/") 
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

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_servidor']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS SERVIDORES')
        return resp
    else:
        return HttpResponseRedirect("/controle/restrito/servidor/consulta/")

def relatorio_excel(request):
    header = ['Header 1', 'Header 2', 'Header 3', 'Header 4']
    return relatorio_base_excel('nome',header ,request.session['relatorio_servidor'])
    

def validacao(request_form):
    warning = True
    if request_form.POST['nmservidor'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe nome do servidor')
        warning = False
    return warning
