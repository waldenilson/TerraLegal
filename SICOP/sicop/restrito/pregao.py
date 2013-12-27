from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormContrato
from django.contrib import messages
from sicop.models import Tbcontrato, AuthUser, Tbpregao
from django.http.response import HttpResponseRedirect, HttpResponse
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_pdf_base_consulta,\
    relatorio_csv_base_consulta, relatorio_ods_base_consulta

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nrpregao']
        descricao = request.POST['dspregao']
        lista = Tbpregao.objects.all().filter( nrpregao__icontains=num, dspregao__icontains=descricao, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbpregao.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_pregao'] = lista
    return render_to_response('sicop/restrito/pregao/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_pregao = Tbpregao(
                                        nrpregao = request.POST['nrpregao'],
                                        dspregao = request.POST['dspregao'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_pregao.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/pregao/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/pregao/cadastro.html',
                               context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbpregao, id=id)
    if request.method == "POST":
        if validacao(request):
            f_pregao = Tbpregao(
                                        id = instance.id,
                                        nrpregao = request.POST['nrpregao'],
                                        dspregao = request.POST['dspregao'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_pregao.save()
            return HttpResponseRedirect("/sicop/restrito/pregao/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/pregao/edicao.html', {"pregao":instance}, context_instance = RequestContext(request))

def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_pregao']
    if lista:
        resp = relatorio_pdf_base_consulta(request, lista, 'RELATORIO DOS PREGOES')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/pregao/consulta/")

def relatorio_ods(request):
    return relatorio_ods_base_consulta(request, 
                                       request.session['relatorio_pregao'], 
                                       'RELATORIO DOS PREGOES',
                                       '/sicop/restrito/pregao/consulta/')

def relatorio_csv(request):
    return relatorio_csv_base_consulta(request, 
                                       request.session['relatorio_pregao'], 
                                       'RELATORIO DOS PREGOES',
                                       '/sicop/restrito/pregao/consulta/')

def validacao(request_form):
    warning = True
    if request_form.POST['nrpregao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o numero do pregao')
        warning = False
    return warning
