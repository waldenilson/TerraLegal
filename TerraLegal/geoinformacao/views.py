#--coding: utf-8
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpRequest
from django.template import loader, Context
import os
from TerraLegal.core.funcoes import upload_file
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from utils import reader_ods
from os.path import abspath, join, dirname
from django.contrib import messages
from TerraLegal.geoinformacao.models import TbparcelaGeo
from TerraLegal.core.funcoes import reader_csv

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def lista(request):
    return render_to_response('lista.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def importar_vw_parcelas(request):
	if request.method == 'POST' and request.FILES:
		path = abspath(join(dirname(__file__), '../../staticfiles'))+'/doc/upload/vw_parcelas.csv'
		res = upload_file(request.FILES['arquivo'],path,request.FILES['arquivo'].name,'csv')
		if res == '0':
			messages.add_message(request,messages.ERROR,'Erro no upload. Tente novamente.')
		elif res == '2':
			messages.add_message(request,messages.WARNING,'Arquivo com extensão incorreta.')
		elif res == '1':
			lines = reader_csv(path, request.POST['delimitador'])
			print 'total de registros: '+str(len(lines))

	return render_to_response('importacao.html',{}, context_instance = RequestContext(request))
