from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpRequest
from django.template import loader, Context
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required

@permission_required('sicop.peca_tecnica_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def lista(request):
    return render_to_response('lista.html',{}, context_instance = RequestContext(request))
