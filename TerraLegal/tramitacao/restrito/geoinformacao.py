from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.gis.geos import GEOSGeometry
import datetime

def glebas_federais(request):
	print datetime.datetime.now()
	particular = Roads.objects.filter( regional = 'MA' )
	assentamento = Roads.objects.filter( regional = 'MA', natureza='Assentamento' )
	#sobre_pa = []
	#for pa in assentamento:
	#	obj = GEOSGeometry(pa.geom)
	#	for p in particular:
	#		if obj.overlaps(p.geom):
	#			sobre_pa.append(pa)
	#			sobre_pa.append(p)
	print datetime.datetime.now()
	return render_to_response('sicop/geoinformacao/glebas_federais.html',
		{'geo':particular}, context_instance = RequestContext(request))

def openlayers(request):
	return render_to_response('sicop/geoinformacao/kml.html',
		{}, context_instance = RequestContext(request))
