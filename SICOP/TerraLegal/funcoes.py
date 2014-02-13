from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context

from django.http.response import HttpResponseRedirect, HttpResponse
from sicop.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia, Tbpregao,\
    Tbdivisao
from sicop.forms import FormProcessoRural, FormProcessoUrbano,\
    FormProcessoClausula
from sicop.restrito import processo_rural
from types import InstanceType
from sicop.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
from sicop.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header

from django.contrib.auth.models import Permission
from sicop import admin


def verificaDivisaoUsuario(request):
    print 'VerificaDivisaoUsuario'
    classe_divisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao.nrclasse
    print request.user.id
    print classe_divisao
    
    divisoes = []
    p_divisoes = Tbdivisao.objects.filter(nrclasse__lte = classe_divisao )
    
    for obj in p_divisoes:
        divisoes.append(obj)

    for obj in divisoes:
        print obj.nmdivisao,obj.id,obj.nrclasse
    
    return (divisoes); 
        
