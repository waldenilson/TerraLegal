from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormProcessos, FormSubArea
from sicop.models import Tbsubarea
from django.http import HttpResponseRedirect
from django.contrib import messages

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nmsubarea']
        lista = Tbsubarea.objects.all().filter( nmsubarea__contains=num )
    else:
        lista = Tbsubarea.objects.all()
    lista = lista.order_by( 'id' )
    return render_to_response('sicop/restrito/sub_area/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
def cadastro(request):
    if request.method == "POST":
        form = FormSubArea(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/") 
    else:
        form = FormSubArea()
    return render_to_response('sicop/restrito/sub_area/cadastro.html',{"form":form}, context_instance = RequestContext(request))

@login_required
def edicao(request, id):
    instance = get_object_or_404(Tbsubarea, id=id)
    if request.method == "POST":
        form = FormSubArea(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")
    else:
        form = FormSubArea(instance=instance)
    return render_to_response('sicop/restrito/sub_area/edicao.html', {"form":form}, context_instance = RequestContext(request))


def validacao(request_form):
    warning = True
    if request_form.POST['nmsubarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a sub area')
        warning = False
    return warning