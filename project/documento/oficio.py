from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from project.tramitacao.models import AuthUser
from project.documento.models import Oficio
from django.contrib import messages
from project.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse

from odslib import ODS
import datetime
from project.core.funcoes import format_datetime, gerar_pdf,mes_do_ano_texto
from os.path import abspath, join, dirname
from project import settings
from django.db.models import Q

@permission_required('documento.oficio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    lista = []
    if request.method == "POST":
        numero = request.POST['numero']
        if request.POST['numero'] != '':
            lista = Oficio.objects.filter( numero__icontains=numero)
            lista = lista.order_by( '-data_documento' )
        texto = request.POST['texto']
        if texto != '':
            lista = Oficio.objects.filter(
                Q( assunto__icontains=texto )|
                Q( mensagem__icontains=texto )|
                Q( remetente__icontains=texto )|
                Q( nome_destinatario__icontains=texto )|
                Q( localidade__icontains=texto )|
                Q( signatario__icontains=texto )|                
                Q( cargo_signatario__icontains=texto )|
                Q( data_documento__icontains=texto )
            )
            lista = lista.order_by( '-data_documento' )

    return render_to_response('documento/oficio/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    
@permission_required('documento.oficio_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    if request.method == "POST":
        f_obj = Oficio(
            numero = request.POST['numero'],
            mensagem = request.POST['mensagem'],
            auth_user = AuthUser.objects.get( pk = request.user.id ),
            localidade = request.POST['localidade'],
            assunto = request.POST['assunto'],
            remetente = request.POST['remetente'],
            nome_destinatario = request.POST['nome_destinatario'].upper(),
            cargo_destinatario = request.POST['cargo_destinatario'],
            empresa_destinatario = request.POST['empresa_destinatario'],
            cidade_destinatario = request.POST['cidade_destinatario'],
            uf_destinatario = request.POST['uf_destinatario'],
            cep_destinatario = request.POST['cep_destinatario'],
            signatario = request.POST['signatario'].upper(),
            cargo_signatario = request.POST['cargo_signatario'].title(),
            data_cadastro = datetime.datetime.now()
        )        
        dt = request.POST['data_documento'].split('/')
        f_obj.data_documento = datetime.datetime(day=int(dt[0]),month=int(dt[1]),year=int(dt[2]))
        f_obj.save()
        
        dados = {
            'brasao':abspath(join(dirname(__file__), '../../staticfiles'))+'/img/slide_1.jpg',
            'numero':f_obj.numero,
            'assunto':f_obj.assunto,
            'mensagem':f_obj.mensagem,
            'remetente':f_obj.remetente,
            'destinatario':f_obj.nome_destinatario,
            'cargo':f_obj.cargo_destinatario,
            'empresa':f_obj.empresa_destinatario,
            'cidade':f_obj.cidade_destinatario,
            'estado':f_obj.uf_destinatario,
            'cep':f_obj.cep_destinatario,
            'localidade':f_obj.localidade,
            'dia':dt[0],
            'mes':mes_do_ano_texto(int(dt[1])),
            'ano':dt[2],
            'signatario':f_obj.signatario,
            'cargo_signatario':f_obj.cargo_signatario
        }
        return gerar_pdf(request,'/documento/oficio/oficio.html',dados, settings.MEDIA_ROOT+'/tmp','oficio.pdf')

    return render_to_response('documento/oficio/cadastro.html',{'data_hoje':format_datetime(datetime.datetime.now()).replace('/','')}, context_instance = RequestContext(request))

@permission_required('documento.oficio_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    instance = get_object_or_404(Oficio, id=id)
    if request.method == "POST":

        if not request.user.has_perm('documento.oficio_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/') 

        f_obj = Oficio(
            id = instance.id,
            numero = request.POST['numero'],
            mensagem = request.POST['mensagem'],
            auth_user = AuthUser.objects.get( pk = request.user.id ),
            localidade = request.POST['localidade'],
            assunto = request.POST['assunto'],
            remetente = request.POST['remetente'],
            nome_destinatario = request.POST['nome_destinatario'].upper(),
            cargo_destinatario = request.POST['cargo_destinatario'],
            empresa_destinatario = request.POST['empresa_destinatario'],
            cidade_destinatario = request.POST['cidade_destinatario'],
            uf_destinatario = request.POST['uf_destinatario'],
            cep_destinatario = request.POST['cep_destinatario'],
            signatario = request.POST['signatario'].upper(),
            cargo_signatario = request.POST['cargo_signatario'].title(),
            data_cadastro = instance.data_cadastro
        )

        dt = request.POST['data_documento'].split('/')
        f_obj.data_documento = datetime.datetime(day=int(dt[0]),month=int(dt[1]),year=int(dt[2]))

        f_obj.save()
        #return HttpResponseRedirect("/documento/oficio/edicao/"+str(id)+"/")
        dados = {
            'brasao':abspath(join(dirname(__file__), '../../staticfiles'))+'/img/slide_1.jpg',
            'numero':f_obj.numero,
            'assunto':f_obj.assunto,
            'mensagem':f_obj.mensagem,
            'remetente':f_obj.remetente,
            'destinatario':f_obj.nome_destinatario,
            'cargo':f_obj.cargo_destinatario,
            'empresa':f_obj.empresa_destinatario,
            'cidade':f_obj.cidade_destinatario,
            'estado':f_obj.uf_destinatario,
            'cep':f_obj.cep_destinatario,
            'localidade':f_obj.localidade,
            'dia':dt[0],
            'mes':mes_do_ano_texto(int(dt[1])),
            'ano':dt[2],
            'signatario':f_obj.signatario,
            'cargo_signatario':f_obj.cargo_signatario
        }
        return gerar_pdf(request,'/documento/oficio/oficio.html',dados, settings.MEDIA_ROOT+'/tmp','oficio.pdf')

    return render_to_response('documento/oficio/edicao.html', {"oficio":instance}, context_instance = RequestContext(request))
