#coding:utf-8
from django.template.context import RequestContext
from django.shortcuts import render_to_response

@permission_required('documento.documento_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def lista(request):
    return render_to_response('documento/lista.html',{}, context_instance = RequestContext(request))
