from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormGleba, FormPendencia
from sicop.models import Tbgleba, Tbsubarea, Tbpendencia, Tbtipopendencia,\
    Tbstatuspendencia
from django.http.response import HttpResponseRedirect
from django.contrib import messages

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, pendencia):
    tipopendencia = Tbtipopendencia.objects.all().order_by("dspendencia")
    statuspendencia = Tbstatuspendencia.objects.all()
    instance = get_object_or_404(Tbpendencia, id=pendencia)
    
    if request.method == "POST":
        if validacao(request):
            f_pendencia = Tbpendencia(
                                       id = instance.id,
                                       auth_user = instance.auth_user,
                                       tbprocessobase = instance.tbprocessobase,
                                       dsdescricao = request.POST['dsdescricao'],
                                       dtpendencia = instance.dtpendencia,
                                       tbtipopendencia = Tbtipopendencia.objects.get( pk = request.POST['tbtipopendencia'] ),
                                       tbstatuspendencia = Tbstatuspendencia.objects.get( pk = request.POST['tbstatuspendencia'] ) 
                                      )
            f_pendencia.save()
            return HttpResponseRedirect("/sicop/restrito/processo/consulta/")
     
    return render_to_response('sicop/restrito/pendencia/edicao.html', 
                              {"pendencia":instance,'tipopendencia':tipopendencia,
                               'statuspendencia':statuspendencia}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['dsdescricao'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a descricao da pendencia.')
        warning = False
    return warning
