from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages
from sicop.forms import FormPecasTecnicas
from sicop.models import Tbpecastecnicas, Tbgleba, Tbcaixa, Tbcontrato,\
    Tbprocessobase, Tbprocessorural, AuthUser, Tbdivisao, AuthGroup,\
    AuthUserGroups, Tbservidor
import datetime
from django.contrib.auth.hashers import make_password, load_hashers, get_hasher
import json
from collections import OrderedDict
from django.http.response import HttpResponse
from sicop.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
from sicop.admin import verificar_permissao_grupo

nome_relatorio      = "relatorio_usuario"
response_consulta  = "/sicop/restrito/usuario/consulta/"
titulo_relatorio    = "Relatorio Usuarios"
planilha_relatorio  = "Usuarios"


@permission_required('sicop.usuario_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        print 'User: '+AuthUser.objects.get( pk = request.user.id ).tbdivisao.nmdivisao
        # se usuario for do grupo Super; mostra todos senao mostra somente os usuarios da divisao
        if verificar_permissao_grupo( AuthUser.objects.get( pk = request.user.id ), {'Super'} ):
            lista = AuthUser.objects.all().filter( first_name__icontains=first_name, email__icontains=email )
        else:
            lista = AuthUser.objects.all().filter( first_name__icontains=first_name, email__icontains=email, 
                                                   tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    else:
        # se usuario for do grupo Super; mostra todos senao mostra somente os usuarios da divisao
        if verificar_permissao_grupo( AuthUser.objects.get( pk = request.user.id ), {'Super'} ):
            lista = AuthUser.objects.all()
        else:
            lista = AuthUser.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )

    lista = lista.order_by( 'username' )
    #gravando na sessao o resultado da consulta preparando para o relatorio/pdf
    request.session['relatorio_usuario'] = lista
    return render_to_response('sicop/restrito/usuario/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.usuario_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    
    #servidor = Tbservidor.objects.all()
    divisao = Tbdivisao.objects.all().order_by('nmdivisao')
    
    
    grupo = AuthGroup.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('name')
    
    result = {}
    for obj in grupo:
        result.setdefault(obj.name, False)
    result = sorted(result.items())

    
    ativo = False
    if request.POST.get('is_active',False):
        ativo = True
    
    if request.method == "POST":
        if validacao(request, 'cadastro'):            
            usuario = AuthUser(
                                   tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                   password = make_password(request.POST['password']),
                                   first_name = request.POST['first_name'],
                                   last_name = request.POST['last_name'],
                                   email = request.POST['email'],
                                   username = request.POST['username'],
                                   is_superuser = False,
                                   is_staff = True,
                                   is_active = ativo,
                                   last_login = datetime.datetime.now(),
                                   date_joined = datetime.datetime.now()
                                   )
            usuario.save()
            
            for obj in grupo:
                if request.POST.get(obj.nmservidor, False):
                    #verificar se esse grupo ja esta ligado ao usuario
                        # inserir ao authusergroups
                    ug = AuthUserGroups( user = AuthUser.objects.get( pk = usuario.id ),
                                          group = AuthGroup.objects.get( pk = obj.id ) )
                    ug.save()
            
            return HttpResponseRedirect("/sicop/restrito/usuario/consulta/") 
    
    return render_to_response('sicop/restrito/usuario/cadastro.html',{'divisao':divisao,'result':result}, context_instance = RequestContext(request))


@permission_required('sicop.usuario_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    
    divisao = Tbdivisao.objects.all().order_by('nmdivisao')
    grupo = AuthGroup.objects.all().filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id ).order_by('name')
    userGrupo = AuthUserGroups.objects.all().filter( user = id )
    
    result = {}
    for obj in grupo:
        achou = False
        for obj2 in userGrupo:
            if obj.id == obj2.group.id:
                result.setdefault(obj.name,True)
                achou = True
                break
        if not achou:
            result.setdefault(obj.name, False)
    result = sorted(result.items())
            
    user_obj = get_object_or_404(AuthUser, id=id)

    if request.method == "POST":
        
        if not request.user.has_perm('sicop.usuario_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        # verificando os grupos do usuario
        for obj in grupo:
            if request.POST.get(obj.name, False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                if not res:
                    # inserir ao authusergroups
                    ug = AuthUserGroups( user = AuthUser.objects.get( pk = id ),
                                          group = AuthGroup.objects.get( pk = obj.id ) )
                    ug.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                if res:
                    # excluir do authusergroups
                    for aug in res:
                        aug.delete()
                    #print obj.name + ' desmarcou deste usuario'
                    
        if validacao(request, 'edicao'):
            
            # tratar o campo senha
            senha_digitada = request.POST['password']
            senha_atual = user_obj.password
            if len(senha_digitada) > 2:
                senha_atual = make_password( senha_digitada )
            
            usuario = AuthUser(
                                   id = user_obj.id,
                                   tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                   password = senha_atual,
                                   first_name = request.POST['first_name'],
                                   last_name = request.POST['last_name'],
                                   email = request.POST['email'],
                                   username = request.POST['username'],
                                   is_superuser = user_obj.is_superuser,
                                   is_staff = user_obj.is_staff,
                                   is_active = user_obj.is_active,
                                   last_login = user_obj.last_login,
                                   date_joined = user_obj.date_joined
                                   )
            usuario.save()
            return HttpResponseRedirect("/sicop/restrito/usuario/edicao/"+str(id)+"/")
    
    return render_to_response('sicop/restrito/usuario/edicao.html', 
                              {'result':result,'grupo':grupo,'usergrupo':userGrupo,'user_obj':user_obj,'divisao':divisao}, context_instance = RequestContext(request))


@login_required
def edicao_usuario_logado(request, id):
    
    if str(request.user.id) == str(id):
    
        divisao = Tbdivisao.objects.all()
        grupo = AuthGroup.objects.all()
        #servidor = Tbservidor.objects.all()
        userGrupo = AuthUserGroups.objects.all().filter( user = id )
        
        result = {}
        for obj in grupo:
            achou = False
            for obj2 in userGrupo:
                if obj.id == obj2.group.id:
                    result.setdefault(obj.name,True)
                    achou = True
                    break
            if not achou:
                result.setdefault(obj.name, False)
        result = sorted(result.items())
        
        ativo = False
        if request.POST.get('is_active',False):
            ativo = True
            
        user_obj = get_object_or_404(AuthUser, id=id)
    
        if request.method == "POST":
            
            if request.user.has_perm('sicop.usuario_grupo_edicao'):
                # verificando os grupos do usuario
                for obj in grupo:
                    if request.POST.get(obj.name, False):
                        #verificar se esse grupo ja esta ligado ao usuario
                        res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                        if not res:
                            # inserir ao authusergroups
                            ug = AuthUserGroups( user = AuthUser.objects.get( pk = id ),
                                                  group = AuthGroup.objects.get( pk = obj.id ) )
                            ug.save()
                            #print obj.name + ' nao esta ligado a este usuario'
                    else:
                        #verificar se esse grupo foi desligado do usuario
                        res = AuthUserGroups.objects.all().filter( user = id, group = obj.id )
                        if res:
                            # excluir do authusergroups
                            for aug in res:
                                aug.delete()
                            #print obj.name + ' desmarcou deste usuario'
                        
            if validacao(request, 'edicao'):
                
                # tratar o campo senha
                senha_digitada = request.POST['password']
                senha_atual = user_obj.password
                if len(senha_digitada) > 2:
                    senha_atual = make_password( senha_digitada )
                
                usuario = AuthUser(
                                       id = user_obj.id,
                                       tbdivisao = Tbdivisao.objects.get( pk = request.POST['tbdivisao'] ),
                                       password = senha_atual,
                                       first_name = request.POST['first_name'],
                                       last_name = request.POST['last_name'],
                                       email = request.POST['email'],
                                       username = request.POST['username'],
                                       is_superuser = user_obj.is_superuser,
                                       is_staff = user_obj.is_staff,
                                       is_active = ativo,
                                       last_login = user_obj.last_login,
                                       date_joined = user_obj.date_joined
                                       )
                usuario.save()
                return HttpResponseRedirect("/sicop/restrito/usuario/edicao/usuario/"+str(id)+"/")
        
        return render_to_response('sicop/restrito/usuario/edicao.html', 
                                  {'result':result,'grupo':grupo,'usergrupo':userGrupo,'user_obj':user_obj,'divisao':divisao}, context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect("/sicop/restrito/usuario/edicao/"+str(id)+"/")


@permission_required('sicop.usuario_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','DIVISAO') )
        for obj in lista:
            dados.append( ( obj.username , obj.tbdivisao.nmdivisao ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.usuario_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):

    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Divisao' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        
    #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.username)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbdivisao.nmdivisao)    
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

@permission_required('sicop.usuario_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Divisao'])
        for obj in lista:
            writer.writerow([obj.username, obj.tbdivisao.nmdivisao])
        return response
    else:
        return HttpResponseRedirect( response_consulta )



def validacao(request_form, acao):
    warning = True
    if request_form.POST['first_name'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Nome')
        warning = False
    if request_form.POST['last_name'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Sobrenome')
        warning = False
    if request_form.POST['username'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o Login')
        warning = False
    
#    result = AuthUser.objects.filter( username = request_form.POST['username'], id = request_form.user.id )
#    if result:
#        messages.add_message(request_form,messages.WARNING,'Login usado por outro usuario. Informe um login diferente.')
#        warning = False
    
#    result = AuthUser.objects.filter( first_name = request_form.POST['first_name'], id = request_form.user.id )
#    if result:
#        messages.add_message(request_form,messages.WARNING,'Nome usado por outro usuario. Informe um nome diferente.')
#        warning = False
    
    if acao == 'cadastro':
        if request_form.POST['password'] == '':
            messages.add_message(request_form,messages.WARNING,'Informe a Senha')
            warning = False
    if request_form.POST['tbdivisao'] == '':
        messages.add_message(request_form,messages.WARNING,'Selecione a Divisao')
        warning = False
    return warning
