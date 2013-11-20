from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSituacaoProcesso, FormSituacaoGeo
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from sicop.models import Tbsituacaoprocesso, Tbsituacaogeo, AuthUser
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmsituacaogeo']
        lista = Tbsituacaogeo.objects.all().filter( nmsituacaogeo__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbsituacaogeo.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_situacao_geo'] = lista
    return render_to_response('sicop/restrito/situacao_geo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_situacaogeo = Tbsituacaogeo(
                                                nmsituacaogeo = request.POST['nmsituacaogeo'],
                                                dssituacaogeo = request.POST['dssituacaogeo'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_situacaogeo.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/situacao_geo/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/situacao_geo/cadastro.html', context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbsituacaogeo, id=id)
    if request.method == "POST":
        if validacao(request):
            f_situacaogeo = Tbsituacaogeo(
                                                id = instance.id,
                                                nmsituacaogeo = request.POST['nmsituacaogeo'],
                                                dssituacaogeo = request.POST['dssituacaogeo'],
                                                tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                            )
            f_situacaogeo.save()
            return HttpResponseRedirect("/sicop/restrito/situacao_geo/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/situacao_geo/edicao.html', {"situacaogeo":instance}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_situacao_geo']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS SITUACOES GEO')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/situacao_geo/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmsituacaogeo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da situacao geo')
        warning = False
    return warning
