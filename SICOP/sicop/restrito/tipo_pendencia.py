from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormTipoPendencia
from sicop.models import Tbtipopendencia
from django.http.response import HttpResponseRedirect
from django.contrib import messages

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['dspendencia']
        lista = Tbtipopendencia.objects.all().filter( dspendencia__contains=nome )
    else:
        lista = Tbtipopendencia.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/tipo_pendencia/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormTipoPendencia(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/tipo_pendencia/consulta/") 
    else:
        form = FormTipoPendencia()
    return render_to_response('sicop/restrito/tipo_pendencia/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbtipopendencia, id=id)
    if request.method == "POST":
        form = FormTipoPendencia(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/tipo_pendencia/consulta/")
    else:
        form = FormTipoPendencia(instance=instance) 
    return render_to_response('sicop/restrito/tipo_pendencia/edicao.html', {"form":form}, context_instance = RequestContext(request))

def validacao(request_form):
    warning = True
    if request_form.POST['dspendencia'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do tipo pendencia')
        warning = False
    return warning
