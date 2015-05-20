from TerraLegal.tramitacao.models import Glebaspublicas
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def glebas_federais(request):
	geo = Glebaspublicas.objects.filter( sr4 = '12' )
	return render_to_response('sicop/geoinformacao/kml.html',
		{'geo':geo}, context_instance = RequestContext(request))

def openlayers(request):
	return render_to_response('sicop/geoinformacao/openlayers.html',
		{}, context_instance = RequestContext(request))
