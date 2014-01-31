from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.forms import FormStatusPendencia, FormAuthGroup
from sicop.models import Tbstatuspendencia, AuthGroup, AuthPermission,\
    AuthGroupPermissions, AuthUser
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from sicop.admin import verificar_permissao_grupo
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS

nome_relatorio      = "relatorio_grupo"
response_consulta  = "/sicop/restrito/grupo/consulta/"
titulo_relatorio    = "Relatorio Grupos"
planilha_relatorio  = "Grupos"


@permission_required('sicop.grupo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    if request.method == "POST":
        nome = request.POST['name']
        lista = AuthGroup.objects.all().filter( name__icontains=nome, tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        lista = AuthGroup.objects.all().filter(tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id)
    lista = lista.order_by( 'name' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_grupo'] = lista
    return render_to_response('sicop/restrito/grupo/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.grupo_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        next = request.GET.get('next', '/')    
        if validacao(request):
            f_grupo = AuthGroup(
                                        name = request.POST['nome'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_grupo.save()
            if next == "/":
                return HttpResponseRedirect("/sicop/restrito/grupo/consulta/")
            else:    
                return HttpResponseRedirect( next ) 
    return render_to_response('sicop/restrito/grupo/cadastro.html',{}, context_instance = RequestContext(request))
    
@permission_required('sicop.grupo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):

    permissao = AuthPermission.objects.all().order_by('name')
    grupoPermissao = AuthGroupPermissions.objects.all().filter( group = id )

    result = {}
    for obj in permissao:
        achou = False
        for obj2 in grupoPermissao:
            if obj.id == obj2.permission.id:
                result.setdefault(obj.name,True)
                achou = True
                break
        if not achou:
            result.setdefault(obj.name, False)
    result = sorted(result.items())

    
    instance = get_object_or_404(AuthGroup, id=id)
    if request.method == "POST":
        
        if not request.user.has_perm('sicop.grupo_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 


        # verificando os grupos do usuario
        for obj in permissao:
            if request.POST.get(obj.name, False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = AuthGroupPermissions.objects.all().filter( group = id, permission = obj.id )
                if not res:
                    # inserir ao authusergroups
                    ug = AuthGroupPermissions( group = AuthGroup.objects.get( pk = id ),
                                          permission = AuthPermission.objects.get( pk = obj.id ) )
                    ug.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = AuthGroupPermissions.objects.all().filter( group = id, permission = obj.id )
                if res:
                    # excluir do authusergroups
                    for aug in res:
                        aug.delete()
                    #print obj.name + ' desmarcou deste usuario'        
        
        if validacao(request):
            f_grupo = AuthGroup(
                                        id = instance.id,
                                        name = request.POST['nome'],
                                        tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                      )
            f_grupo.save()
            return HttpResponseRedirect("/sicop/restrito/grupo/edicao/"+str(id)+"/")
    return render_to_response('sicop/restrito/grupo/edicao.html', {"grupo":instance,'result':result,'permissao':permissao,'grupopermissao':grupoPermissao}, context_instance = RequestContext(request))


@permission_required('sicop.grupo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','') )
        for obj in lista:
            dados.append( ( obj.name , '' ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.grupo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.name)
            x += 1
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA     
       
        relatorio_ods_base(ods, planilha_relatorio)
        # generating response
        response = HttpResponse(mimetype=ods.mimetype.toString())
        response['Content-Disposition'] = 'attachment; filename='+nome_relatorio+'.ods'
        ods.save(response)
    
        return response
    else:
        return HttpResponseRedirect( response_consulta )

@permission_required('sicop.grupo_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome'])
        for obj in lista:
            writer.writerow([obj.name])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form):
    warning = True
    if request_form.POST['nome'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do grupo')
        warning = False
    return warning
