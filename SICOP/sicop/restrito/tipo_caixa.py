from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoCaixa
from django.http import HttpResponseRedirect
from sicop.models import Tbtipocaixa, AuthUser
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmtipocaixa']
        lista = Tbtipocaixa.objects.all().filter( nmtipocaixa__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbtipocaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_tipo_caixa'] = lista
    return render_to_response('sicop/restrito/tipo_caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')    
        if validacao(request):
            f_tipocaixa = Tbtipocaixa(
                                        nmtipocaixa = request.POST['nmtipocaixa'],
                                        desctipocaixa = request.POST['desctipocaixa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipocaixa.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/tipo_caixa/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/tipo_caixa/cadastro.html',{}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbtipocaixa, id=id)
    if request.method == "POST":
        if validacao(request):
            f_tipocaixa = Tbtipocaixa(
                                        id = instance.id,
                                        nmtipocaixa = request.POST['nmtipocaixa'],
                                        desctipocaixa = request.POST['desctipocaixa'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_tipocaixa.save()
            return HttpResponseRedirect("/sicop/restrito/tipo_caixa/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/tipo_caixa/edicao.html', {"tipocaixa":instance}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_tipo_caixa']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DOS TIPOS CAIXA')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/tipo_caixa/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmtipocaixa'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para o tipo caixa')
        warning = False
    return warning
