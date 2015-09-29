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
		path = abspath(join(dirname(__file__), '../../media'))+'/tmp/vw_parcelas.csv'
		res = upload_file(request.FILES['arquivo'],path,request.FILES['arquivo'].name,'csv')
		if res == '0':
			messages.add_message(request,messages.ERROR,'Erro no upload. Tente novamente.')
		elif res == '2':
			messages.add_message(request,messages.WARNING,'Arquivo com extensão incorreta.')
		elif res == '1':
			lines = reader_csv(path, request.POST['delimitador'])
			x = 0
			for line in lines:
				print line
				if TbparcelaGeo.objects.filter(id=line[0], identifica=line[11]):
					pass # atualiza
				else:
					# cadastra
					x = x + 1
					obj_parcela = TbparcelaGeo(
							id = line[0],
							nome = line[1],
							gleba = line[2],
							nome_deten = line[3],
							cpf_detent = line[4],
							nr_process = line[5],
							planilha_o = line[6],
#							data_recep = line[7],
							protocolo = line[8],
							status = line[9],
							fronteira = line[10],
							identifica = line[11],
							contrato = line[12],
							id_contrat = line[13],
							empresa = line[14],
							fiscal = line[15],
							email = line[16],
							area_ha_ut = line[17],
#							geom = line[18],
							situacao_p = line[19],
							natureza = line[20],
							migrada = line[21],
							municipio = line[22],
							uf_id = line[23],
							gleba_situ = line[24],
							regional = line[25]
#							data_situacao_processo = line[26]
						)
					if line[7] == '':
						obj_parcela.data_recep = None
					if line[26] == '':
						obj_parcela.data_situacao_processo = None
					obj_parcela.save()
					print str(x)
			print 'total cadastros: '+str(x)
	return render_to_response('importacao.html',{}, context_instance = RequestContext(request))
