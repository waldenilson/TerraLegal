from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormGleba, FormPendencia
from sicop.models import Tbgleba, Tbsubarea, Tbpendencia, Tbtipopendencia,\
    Tbstatuspendencia, Tbdocumentomaterialrme
from django.http.response import HttpResponseRedirect
from django.contrib import messages

@permission_required('servidor.documento_rme_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, materialrme):
    
    instance = get_object_or_404(Tbdocumentomaterialrme, id=materialrme)
    
    if request.method == "POST":
        if validacao(request):
            f_material = Tbdocumentomaterialrme(
                                       id = instance.id,
                                       tbdocumentorme = instance.tbdocumentorme,
                                       especificacao = request.POST['especificacao'],
                                       unidade = request.POST['unidade'],
                                       qtdsolicitada = request.POST['qtdsolicitada']
                                    )
            f_material.save()
            return HttpResponseRedirect("/sicop/restrito/documento/edicao/"+str(instance.tbdocumentorme.tbdocumentobase.id)+"/")
     
    return render_to_response('sicop/restrito/documento_material_rme/edicao.html', 
                              {"material":instance}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['especificacao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a especificacao.')
        warning = False
    if request_form.POST['unidade'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a unidade.')
        warning = False
    if request_form.POST['qtdsolicitada'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade solicitada.')
        warning = False
    return warning
