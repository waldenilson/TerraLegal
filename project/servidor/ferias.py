from django.contrib.auth.decorators import login_required, user_passes_test,\
    permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import messages

from project.tramitacao.forms import FormPecasTecnicas, FormServidor,FormFerias

from project.tramitacao.models import Tbpecastecnicas, Tbgleba, Tbcaixa,Tbcontrato, Tbservidor, AuthUser, Tbdivisao, Tbferias, Tbsituacao
from project.tramitacao.admin import verificar_permissao_grupo
from django.http.response import HttpResponse
from project.tramitacao.relatorio_base import relatorio_pdf_base_header,\
    relatorio_pdf_base_header_title, relatorio_pdf_base,\
    relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base
from odslib import ODS
import datetime
from datetime import timedelta
from project.tramitacao.restrito.processo import formatDataToText

from django.shortcuts import render_to_response
import random
import time

    
@permission_required('servidor.servidor_cadastro_ferias', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastroferias(request,id): #id se refere ao servidor
    servidor = Tbservidor.objects.filter(id = id)
    ferias   = Tbferias.objects.all().filter(tbservidor=id)
    situacao = Tbsituacao.objects.all().filter(cdTabela="ferias")
    
    if request.method == "POST":
            stAntecipa = False
            if request.POST.get('stAntecipa',False):
                stAntecipa = True
            stDecimoTerceiro = False
            if request.POST.get('stDecimoTerceiro',False):
                stDecimoTerceiro = True
            
            dtInicio1 = None
            if request.POST['dtInicio1']:
                dtInicio1 = datetime.datetime.strptime( request.POST['dtInicio1'], "%d/%m/%Y")
            dtInicio2 = None
            if request.POST['dtInicio2']:
                dtInicio2 = datetime.datetime.strptime( request.POST['dtInicio2'], "%d/%m/%Y")
            dtInicio3 = None
            if request.POST['dtInicio3']:
                dtInicio3 = datetime.datetime.strptime( request.POST['dtInicio3'], "%d/%m/%Y")
            
            nrDias1 = request.POST['nrDias1']
            if not request.POST['nrDias1']:
                nrDias1 = None
            nrDias2 = request.POST['nrDias2']
            if not request.POST['nrDias2']:
                nrDias2 = None
            nrDias3 = request.POST['nrDias3']
            if not request.POST['nrDias3']:
                nrDias3 = None
                
            f_ferias = Tbferias(
                    tbservidor_id = id,
                    nrAno = request.POST['nrAno'],
                    dtInicio1 = dtInicio1,
                    nrDias1 = nrDias1,
                    stSituacao1 = Tbsituacao.objects.get( pk = request.POST['tbsituacao1'] ),
                    dtInicio2 = dtInicio2,
                    nrDias2 = nrDias2,
                    stSituacao2 = Tbsituacao.objects.get( pk = request.POST['tbsituacao2'] ),
                    dtInicio3 = dtInicio3,
                    nrDias3 = nrDias3,
                    stSituacao3 = Tbsituacao.objects.get( pk = request.POST['tbsituacao3'] ),
                    stAntecipa = stAntecipa,
                    stDecimoTerceiro = stDecimoTerceiro,
                    
                    )
            f_ferias.save()
            #colocar aqui uma chamada para as ferias cadastradas do servido
            return HttpResponseRedirect("/servidor/consulta/")
    else:
            return render_to_response('controle/servidor/cadastroFerias.html',{'servidor':servidor,'ferias':ferias,'situacao':situacao}, context_instance = RequestContext(request))

@permission_required('servidor.servidor_edicao_ferias', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicaoferias(request, id): #esse id se refere as ferias
    ferias = get_object_or_404(Tbferias, id=id)
    servidor = Tbservidor.objects.get(id = Tbferias.objects.get(pk = id).tbservidor_id)
    situacao = Tbsituacao.objects.all().filter(cdTabela="ferias")
    
    dtInicio1 = formatDataToText(ferias.dtInicio1)
    dtInicio2 = formatDataToText(ferias.dtInicio2)
    dtInicio3 = formatDataToText(ferias.dtInicio3)
 
    if ferias.nrDias1 == None:
        ferias.nrDias1 = ""
        dtFim1 = ""
    else:
        dtFim1 = formatDataToText(ferias.dtInicio1 + timedelta(ferias.nrDias1 - 1))
        
    
    if ferias.nrDias2 == None:
        ferias.nrDias2 = ""
        dtFim2 = ""
    else:
        dtFim2 = formatDataToText(ferias.dtInicio2 + timedelta(ferias.nrDias2 - 1))
    
    if ferias.nrDias3 == None:
        ferias.nrDias3 = ""
        dtFim3 = ""
    else:
        dtFim3 = formatDataToText(ferias.dtInicio3 + timedelta(ferias.nrDias3 - 1))
        
    if request.method == "POST":
        if validacao(request):
            stAntecipa = False
            if request.POST.get('stAntecipa',False):
                stAntecipa = True
            stDecimoTerceiro = False
            if request.POST.get('stDecimoTerceiro',False):
                stDecimoTerceiro = True
        
            dtInicio1 = None
            if request.POST['dtInicio1']:
                dtInicio1 = datetime.datetime.strptime( request.POST['dtInicio1'], "%d/%m/%Y")
            dtInicio2 = None
            if request.POST['dtInicio2']:
                dtInicio2 = datetime.datetime.strptime( request.POST['dtInicio2'], "%d/%m/%Y")
            dtInicio3 = None
            if request.POST['dtInicio3']:
                dtInicio3 = datetime.datetime.strptime( request.POST['dtInicio3'], "%d/%m/%Y")
                 
            nrDias2 = request.POST['nrDias2']
            if nrDias2 == "":
                nrDias2 = None
       
            nrDias3 = request.POST['nrDias3']
            if nrDias3 == "":
                nrDias3 = None
            f_ferias = Tbferias(
                        id = ferias.id,# se nao colocar essa linha ele cria um novo
                        tbservidor_id = servidor.id,
                        nrAno = request.POST['nrAno'],
                        dtInicio1 = dtInicio1,
                        nrDias1 = request.POST['nrDias1'],
                        stSituacao1 = Tbsituacao.objects.get( pk = request.POST['tbsituacao1']),
                        dtInicio2 = dtInicio2,
                        nrDias2 = nrDias2,
                        stSituacao2 = Tbsituacao.objects.get( pk = request.POST['tbsituacao2']),
                        dtInicio3 = dtInicio3,
                        nrDias3 = nrDias3,
                        stSituacao3 = Tbsituacao.objects.get( pk = request.POST['tbsituacao3']),
                        stAntecipa = stAntecipa,
                        stDecimoTerceiro = stDecimoTerceiro,
                        
                        )
            f_ferias.save()
            return HttpResponseRedirect("/servidor/edicao/"+str(servidor.id)+"/")
    return render_to_response('controle/servidor/edicaoFerias.html',{'ferias':ferias,'servidor':servidor,'dtInicio1':dtInicio1,'dtInicio2':dtInicio2,'dtInicio3':dtInicio3,'situacao':situacao,'dtFim1':dtFim1,'dtFim2':dtFim2,'dtFim3':dtFim3},context_instance = RequestContext(request))



def validacao(request_form):
    warning = True
    if request_form.POST['nrDias1'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe a quantidade de dias do 1o. periodo')
        warning = False
    return warning

def demo_linewithfocuschart(request):
    """
    linewithfocuschart page
    """
    nb_element = 100
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)

    xdata = range(nb_element)
    xdata = map(lambda x: start_time + x * 1000000000, xdata)
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = map(lambda x: x * 2, ydata)
    ydata3 = map(lambda x: x * 3, ydata)
    ydata4 = map(lambda x: x * 4, ydata)

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                   "date_format": tooltip_date}
    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
        'name3': 'series 3', 'y3': ydata3, 'extra3': extra_serie,
        'name4': 'series 4', 'y4': ydata4, 'extra4': extra_serie
    }
    charttype = "lineWithFocusChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }
    return render_to_response('controle/servidor/linewithfocuschart.html', data)
