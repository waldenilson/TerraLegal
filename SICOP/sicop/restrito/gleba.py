from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormGleba
from sicop.models import Tbgleba, Tbsubarea, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo
import xlwt

@login_required
def consulta(request):
    if request.method == "POST":
        nome = request.POST['nmgleba']
        lista = Tbgleba.objects.all().filter( nmgleba__icontains=nome, tbsubarea__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbgleba.objects.all().filter( tbsubarea__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_gleba'] = lista
    return render_to_response('sicop/restrito/gleba/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    subarea = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    if request.method == "POST":
        next = request.GET.get('next', '/')
        form = FormGleba(request.POST)
        if validacao(request):
            if form.is_valid():
                form.save()
                if next == "/":
                    return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")
                else:    
                    return HttpResponseRedirect( next ) 
    else:
        form = FormGleba()
    return render_to_response('sicop/restrito/gleba/cadastro.html',{"form":form,'subarea':subarea}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    subarea = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    instance = get_object_or_404(Tbgleba, id=id)
    if request.method == "POST":
        form = FormGleba(request.POST,request.FILES,instance=instance)
        if validacao(request):
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/sicop/restrito/gleba/edicao/"+str(id)+"/")
    else:
        form = FormGleba(instance=instance) 
    return render_to_response('sicop/restrito/gleba/edicao.html', {"form":form,'subarea':subarea}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_gleba']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS GLEBAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/gleba/consulta/")

def relatorio_excel(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')  
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    # write the header
    header = ['Header 1', 'Header 2', 'Header 3', 'Header 4']
    for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
           sheet.write(0, hcol, hcol_data, style=xlwt.Style.default_style)
 
    # write your data, you can also get it from your model
    data = ['genius', 'super', 'gorgeous', 'awesomeness']
    for row, row_data in enumerate(data, start=1): # start from row no.1
           for col, col_data in enumerate(row_data):
                 sheet.write(row, col, col_data, style=xlwt.Style.default_style)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=my_data.xls'
    book.save(response)
    return response


def validacao(request_form):
    warning = True
    if request_form.POST['nmgleba'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome da gleba')
        warning = False
    return warning
