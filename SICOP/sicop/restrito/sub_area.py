from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormSubArea
from sicop.models import Tbsubarea, AuthUser
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_base_consulta
from sicop.admin import verificar_permissao_grupo
import xlwt
from django.http.response import HttpResponse

@login_required
def consulta(request):
    if request.method == "POST":
        num = request.POST['nmsubarea']
        lista = Tbsubarea.objects.all().filter( nmsubarea__icontains=num, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = Tbsubarea.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    lista = lista.order_by( 'id' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_sub_area'] = lista
    return render_to_response('sicop/restrito/sub_area/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validacao(request):
            f_subarea = Tbsubarea(
                                        nmsubarea = request.POST['nmsubarea'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_subarea.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/sub_area/cadastro.html',{}, context_instance = RequestContext(request))

@login_required
@user_passes_test( lambda u: verificar_permissao_grupo(u, {'Super','Administrador'}), login_url='/excecoes/permissao_negada/')
def edicao(request, id):
    instance = get_object_or_404(Tbsubarea, id=id)
    if request.method == "POST":
        if validacao(request):
            f_subarea = Tbsubarea(
                                        id = instance.id,
                                        nmsubarea = request.POST['nmsubarea'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_subarea.save()
            return HttpResponseRedirect("/sicop/restrito/sub_area/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/sub_area/edicao.html', {"subarea":instance}, context_instance = RequestContext(request))

def relatorio(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session['relatorio_sub_area']
    if lista:
        resp = relatorio_base_consulta(request, lista, 'RELATORIO DAS SUB AREAS')
        return resp
    else:
        return HttpResponseRedirect("/sicop/restrito/sub_area/consulta/")

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
    if request_form.POST['nmsubarea'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um nome para a sub area')
        warning = False
    return warning