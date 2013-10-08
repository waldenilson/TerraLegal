from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbcaixa, Tbtipocaixa, AuthUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.forms import FormCaixa
from sicop.relatorio_base import relatorio_base_consulta
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import urllib2
import urllib
from urllib import addinfourl

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmlocalarquivo']
        lista = Tbcaixa.objects.all().filter( nmlocalarquivo__contains=nome, tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbcaixa.objects.all().filter( tbtipocaixa__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_caixa'] = lista
    return render_to_response('sicop/restrito/caixa/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    tipocaixa = Tbtipocaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormCaixa(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/caixa/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormCaixa()
    return render_to_response('sicop/restrito/caixa/cadastro.html',{"form":form,"tipocaixa":tipocaixa}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    tipocaixa = Tbtipocaixa.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    instance = get_object_or_404(Tbcaixa, id=id)
    if request.method == "POST":
        form = FormCaixa(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/caixa/consulta/")
    else:
        form = FormCaixa(instance=instance)
    return render_to_response('sicop/restrito/caixa/edicao.html', {"form":form,"tipocaixa":tipocaixa}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_caixa']

    dados = []
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    for obj in lista:
        dados.append( Paragraph( obj.nmlocalarquivo , styles["Normal"]) )
        dados.append(Spacer(100,1))
        dados.append( Paragraph( obj.tbtipocaixa.nmtipocaixa , styles["Normal"]) )
        dados.append(Spacer(1,12))

    if lista:
        resp = relatorio_base_consulta(request, dados, 'RELATORIO DAS CAIXAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/caixa/consulta/")

def validacao(request_form):
    warning = True
    if request_form.POST['nmlocalarquivo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a caixa')
        warning = False
    return warning