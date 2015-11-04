# coding: utf-8
from TerraLegal.geoinformacao.models import TbparcelaGeo
from TerraLegal.tramitacao.models import Tbprocessorural, Tbprocessoclausula, Tbmunicipio
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages



nome_relatorio      = "relatorio_parcela"
response_consulta  = "/geoinformacao/parcela/consulta/"
titulo_relatorio    = "Relatorio Parcelas"
planilha_relatorio  = "Parcelas"


#PECAS TECNICAS -----------------------------------------------------------------------------------------------------------------------------

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    lista = []
    if request.method == "POST":
        requerente = request.POST['requerente']
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        
        if len(requerente) >= 3:
            #lista = Tbpecastecnicas.objects.all().filter( nmrequerente__icontains=requerente, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmrequerente')
            lista = TbparcelaGeo.objects.filter( nome_deten__icontains=requerente).order_by('nome_deten')
        else:
            if len(requerente) > 0 and len(requerente) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo Requerente.')

        if len(cpf) >= 3:
            #lista = Tbpecastecnicas.objects.all().filter( nrcpfrequerente__contains=cpf, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('nmrequerente')
            lista = TbparcelaGeo.objects.filter( cpf_detent__contains=cpf ).order_by('nome_deten')
        else:
            if len(cpf) > 0 and len(cpf) < 3:
                messages.add_message(request,messages.WARNING,'Informe no minimo 3 caracteres no campo CPF.')

#    else:
#        lista = Tbpecastecnicas.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
#    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_parcela'] = lista
    return render_to_response('parcela/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def visualizacao(request, id):

    parcela_obj = get_object_or_404(TbparcelaGeo, gid=id)
        
    processo = Tbprocessorural.objects.filter( nrcpfrequerente = parcela_obj.cpf_detent.replace('.','').replace('-','') )
    if not processo:
        processo = Tbprocessoclausula.objects.filter( nrcpfinteressado = parcela_obj.cpf_detent.replace('.','').replace('-','') )
    if not processo:
        processo = Tbprocessoclausula.objects.filter( nrcpfrequerente = parcela_obj.cpf_detent.replace('.','').replace('-','') )
        
    numero_processo = ''
    if processo:
        processo = processo[0] 
        num = processo.tbprocessobase.nrprocesso
        numero_processo = num[0:5]+'.'+num[5:11]+'/'+num[11:15]+'-'+num[15:17]

    return render_to_response('parcela/visualizacao.html',
                              {'parcela':parcela_obj,'processo':processo, 'numero_processo':numero_processo}, 
                            context_instance = RequestContext(request))
