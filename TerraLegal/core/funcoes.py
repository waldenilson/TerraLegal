# -- coding: utf-8 --
from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context

from django.http.response import HttpResponseRedirect, HttpResponse
from TerraLegal.tramitacao.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia, Tbpregao,\
    Tbdivisao
from TerraLegal.tramitacao.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from TerraLegal.tramitacao.restrito import processo_rural
from types import InstanceType
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
from TerraLegal.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header

from django.contrib.auth.models import Permission
from TerraLegal.tramitacao import admin

from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO

def verificaDivisaoUsuario(request):
    classe_divisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao.nrclasse
    divisoes = []
    id_divisoes = []
    id_uf_classe = []
    
    if Tbdivisao.objects.filter(nrclasse__lt = classe_divisao ):
        #a divisao do usuario logado permite que veja objetos de sua div e das divs de classes menores que a sua
        request.session['isdivisao'] = False
        p_divisoes = Tbdivisao.objects.filter(nrclasse__lte = classe_divisao )
        for obj in p_divisoes:
            divisoes.append(obj)
    else:
        #eh uma divisao regional e/ou possui a menor classe da hierarquia
        request.session['isdivisao'] = True
        #usa a divisao do usuario logado
        divisoes = Tbdivisao.objects.all().filter(id = AuthUser.objects.get(pk = request.user.id ).tbdivisao.id)
    
    for obj in divisoes:
        id_divisoes.append(obj.id)#cria lista com as divisoes que o usuario pode acessar
    for obj in divisoes:
        id_uf_classe.append(obj.tbuf.id)#cria lista com os estados que o usuario pode acessar
    request.session['divisoes'] = id_divisoes
    request.session['uf'] = id_uf_classe
    request.session['classe'] = [1,2,3,4,5,6,7,8,9,10]

def gerar_html2pdf():
    template = get_template('sicop/2pdf.html')
    context = Context({'titulo':'O Título do documento'})
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
    return http.HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
