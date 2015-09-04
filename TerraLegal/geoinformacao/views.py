from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpRequest
from django.template import loader, Context
import os
from TerraLegal.core.funcoes import upload_file_vw_parcelas_ods
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from utils import reader_ods
from os.path import abspath, join, dirname

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def lista(request):
    return render_to_response('lista.html',{}, context_instance = RequestContext(request))

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def importar_vw_parcelas(request):
	if request.method == 'POST' and request.FILES:
		path = abspath(join(dirname(__file__), '../../staticfiles'))+'/doc/upload/vw_parcelas.ods'
		upload_file_vw_parcelas_ods(request.FILES['arquivo'],path,request.FILES['arquivo'].name)
		print reader_ods(path,request.POST['planilha'])
	return render_to_response('importacao.html',{}, context_instance = RequestContext(request))
