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
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon, LinearRing

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
#							geom = MultiPolygon(Polygon('01030000A0421200000100000009000000D540F7FACE4C49C02FFD25388F2414C0C3F5285C8F8A654020E2A60E9C4C49C0D71084950B2914C0AE47E17A1436654056663F539F4C49C050BB1B7A1E2914C0E17A14AE47096540E169BECFFA4C49C00A69594D9D2914C0713D0AD7A3E8664063447011644D49C091AFAEBB112A14C09A9999999929664064909CDDB14D49C06A06BD2A632A14C0D7A3703D0AC76440B59499EB004E49C0921119B0AB2A14C052B81E85EB4964406C01F2D2C54D49C08BC9EFD4F92514C07B14AE47E1AA6440D540F7FACE4C49C02FFD25388F2414C0C3F5285C8F8A6540')),
							situacao_p = line[19],
							natureza = line[20],
							migrada = line[21],
							municipio = line[22],
							uf_id = line[23],
							gleba_situ = line[24],
							regional = line[25],
#							data_situacao_processo = line[26]
						)
					if line[7] != '':
						obj_parcela.data_recep = line[7]
					else:	
						obj_parcela.data_recep = None
						
					if line[26] != '':
						obj_parcela.data_situacao_processo = line[26]
					else:	
						obj_parcela.data_situacao_processo = None
					obj_parcela.save()
					print str(x)
			print 'total cadastros: '+str(x)
	return render_to_response('importacao.html',{}, context_instance = RequestContext(request))
