from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoPendencia
from sicop.models import Tbtipopendencia, AuthUser, Tbtipoprocesso
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['dspendencia']
        lista = Tbtipopendencia.objects.all().filter( dspendencia__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipopendencia.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_pendencia'] = lista
    return render_to_response('sicop/restrito/tipo_pendencia/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    tipoprocesso = Tbtipoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    if request.method == "POST":
        if validacao(request):
            f_tipopendencia = Tbtipopendencia(
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipopendencia.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_pendencia/consulta/") 
    return render_to_response('sicop/restrito/tipo_pendencia/cadastro.html',{'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbtipopendencia, id=id)
    tipoprocesso = Tbtipoprocesso.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    if request.method == "POST":
            f_tipopendencia = Tbtipopendencia(
                                        id = instance.id,
                                        dspendencia = request.POST['dspendencia'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipopendencia.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_pendencia/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/tipo_pendencia/edicao.html', {"tipopendencia":instance,'tipoprocesso':tipoprocesso}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_tipo_pendencia']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS TIPOS DE PENDENCIAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/tipo_pendencia/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['dspendencia'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo pendencia')
        warning = False
    return warning
