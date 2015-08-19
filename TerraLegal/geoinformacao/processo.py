from TerraLegal.geoinformacao.models import Roads
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.gis.geos import GEOSGeometry
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.http import HttpResponseRedirect
from django.db.models import Q

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def processo_parcela_titulo(request):
    if request.method == "POST":
        parcelas = Roads.objects.filter( uf_id = request.POST['regional'] )
        parcelas = parcelas.filter( ~Q(nome__icontains = 'P.A.') )
        parcelas = parcelas.filter( ~Q(nome__startswith = 'PA ') )
        parcelas = parcelas.filter( ~Q(nome_deten__icontains = 'PREFEITURA') )
        parcelas = parcelas.filter( ~Q(cpf_detent__iexact = '00000000000') )

        cor_sem_processo = request.POST['cor_sem_processo']
        cor_com_processo = request.POST['cor_com_processo']
        cor_com_titulo = request.POST['cor_com_titulo']

        return render_to_response('processo/processo_parcela_titulo.html',{"retorno":True,"geo":parcelas,"cor_sem_processo":cor_sem_processo,"cor_com_titulo":cor_com_titulo,"cor_com_processo":cor_com_processo}, context_instance = RequestContext(request))

    return render_to_response('processo/processo_parcela_titulo.html',{"retorno":False}, context_instance = RequestContext(request))

#def openlayers(request):
#    return render_to_response('sicop/geoinformacao/kml.html',
#        {}, context_instance = RequestContext(request))
