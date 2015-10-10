# -- coding: utf-8 --
from django.contrib.auth.decorators import login_required, permission_required,\
    user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext, Context

from django.http.response import HttpResponseRedirect, HttpResponse
from TerraLegal.tramitacao.models import Tbprocessorural, Tbtipoprocesso, Tbprocessourbano,\
    Tbprocessoclausula, Tbprocessobase, Tbcaixa, Tbgleba, Tbmunicipio,\
    Tbcontrato, Tbsituacaoprocesso, Tbsituacaogeo, Tbpecastecnicas, AuthUser,\
    AuthUserGroups, Tbmovimentacao, Tbprocessosanexos, Tbpendencia,\
    Tbclassificacaoprocesso, Tbtipopendencia, Tbstatuspendencia, Tbpregao,\
    Tbdivisao
from types import InstanceType
from TerraLegal.tramitacao.admin import verificar_permissao_grupo
import datetime
from django.contrib import messages
from django.utils import simplejson
from TerraLegal.tramitacao.relatorio_base import relatorio_csv_base, relatorio_ods_base,\
    relatorio_ods_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title, relatorio_pdf_base_header

from django.contrib.auth.models import Permission
from TerraLegal.tramitacao import admin

from django import http
from django.template.loader import get_template
from django.template import Context

#import ho.pisa as pisa
import cStringIO as StringIO
import os,sys,csv
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import loader
from TerraLegal import settings as configuracao
from os.path import abspath, join, dirname
import smtplib

from webodt.shortcuts import render_to
from webodt import shortcuts
from webodt.converters import converter
import webodt

def verificaDivisaoUsuario(request):
    classe_divisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao.nrclasse
    divisoes = []
    id_divisoes = []
    id_uf_classe = []
    
    if Tbdivisao.objects.filter(nrclasse__lt = classe_divisao ):
        #a divisao do usuario logado permite que veja objetos de sua div e das divs de classes menores que a sua
        request.session['isdivisao'] = False
        p_divisoes = Tbdivisao.objects.filter(nrclasse__lte = classe_divisao )
        for obj in p_divisoes:
            divisoes.append(obj)
    else:
        #eh uma divisao regional e/ou possui a menor classe da hierarquia
        request.session['isdivisao'] = True
        #usa a divisao do usuario logado
        divisoes = Tbdivisao.objects.all().filter(id = AuthUser.objects.get(pk = request.user.id ).tbdivisao.id)
    
    for obj in divisoes:
        id_divisoes.append(obj.id)#cria lista com as divisoes que o usuario pode acessar
    for obj in divisoes:
        id_uf_classe.append(obj.tbuf.id)#cria lista com os estados que o usuario pode acessar
    request.session['divisoes'] = id_divisoes
    request.session['uf'] = id_uf_classe
    request.session['classe'] = [1,2,3,4,5,6,7,8,9,10]

def gerar_pdf(request, template_path, data, path, name):
    
    # Render html content through html template with context
    t = loader.get_template(template_path)
    c = Context(data)
    html =  t.render(c)
    file = open(os.path.join(path, name), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file)
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    return HttpResponse(pdf, mimetype='application/pdf')

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % \
                    (sUrl, mUrl))
    return path

def generatePDF(request):
    print "generatePDF"
    
    data = {}
    data['recolhimento'] = "28874-8"
    data['farmer'] = 'Old MacDonald'
    data['animals'] = [('Cow', 'Moo'), ('Goat', 'Baa'), ('Pig', 'Oink')]
            

    # Render html content through html template with context
    print "generate_pdf YYY",data
    template = get_template('portaria23/testePDF.html')
    html  = template.render(Context(data))

    # Write PDF to file
    print"ante file"
    file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)
    print "apos"
    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    return HttpResponse(pdf, mimetype='application/pdf')

def upload_file(request_file,path,nome_arquivo,extensao):
    if nome_arquivo[len(nome_arquivo)-3:len(nome_arquivo)] == extensao:        
        try:
            with open(path, 'wb+') as destination:
                for chunk in request_file.chunks():
                    destination.write(chunk)
                destination.close()
                return '1'
        except:
            return '0'
    else:
        return '2'

def reader_csv(path, delimitador):    
    csv.field_size_limit(sys.maxsize)
    retorno = []
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(delimitador), quotechar='\n')
        for row in spamreader:
            if row:
                retorno.append(row) 
    return retorno

def send_smtp(to, user, pwd, smtp, assunto, msg):
    try:
        smtpserver = smtplib.SMTP_SSL(smtp)
        smtpserver.login(user, pwd)
        header = 'To:' + to + '\n' + 'From: ' + user + '\n' + 'Subject:'+assunto+' \n'
        msg = header + msg
        smtpserver.sendmail(user, to, msg)
        smtpserver.close()
        return True
    except:
        return False

def translate(section, key):
    try:
        file_ini = ConfigParser.ConfigParser()
        file_ini.read( abspath(join(dirname(__file__), '../../../translation/'+config('TRANSLATION',default='default')+'.ini')) )
        return file_ini.get(section,key)
    except:
        return ''

def emitir_documento(nome_template, dados=dict()):
    
    template = webodt.ODFTemplate(nome_template)
#    context = dict(titulo='John Doe')
    document = template.render(Context(dados))

    conv = converter()
    pdf = conv.convert(document, format='pdf')
    document.close()
    return HttpResponse(pdf, mimetype='application/pdf')

# datetime to 00/00/0000
def format_datetime(date_time):
    dia = ''
    if date_time.day < 10:
        dia = '0'+str(date_time.day)
    else:
        dia = date_time.day

    mes = ''
    if date_time.month < 10:
        mes = '0'+str(date_time.month)
    else:
        mes = date_time.month
    retorno = str(dia)+'/'+str(mes)+'/'+str(date_time.year)
    return retorno
