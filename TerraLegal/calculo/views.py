from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.calculo.models import Tbextrato, Tbcalculotitulo, TbtrMensal
from TerraLegal.tramitacao.models import Tbmunicipio, AuthUser
from decimal import Decimal
from datetime import date
from TerraLegal.tramitacao.restrito.processo import formatDataToText
from TerraLegal.core.funcoes import generatePDF
from django.contrib import messages
import datetime
from datetime import timedelta
import time

from django.http import HttpResponse, HttpRequest
from django.template import loader, Context
import os
from django.conf import settings

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import loader

nome_relatorio      = "relatorio_portaria80"
response_consulta  = "/sicop/restrito/portaria80/calculo/"
titulo_relatorio    = "Calculo Portaria 80 - Clausulas Resolutivas"

global juros
global principal_corrigido


@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    p_extrato = []
    if request.method == "POST":
        numero = request.POST['numero'].replace('.','').replace('/','').replace('-','')
        cpf = request.POST['cpf'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['requerente']
        titulo = request.POST['cdtitulo']
        p_extrato = []
        p_extrato = Tbextrato.objects.all().filter(numero_processo__icontains = numero,cpf_req__icontains = cpf,
                                nome_req__icontains = requerente, id_req__icontains = titulo,  situacao_processo__icontains = 'Titulado')
        
        #gravando na sessao o resultado da consulta preparando para o relatorio/pdf'''
        #exibir uma warning informando que o campo data do requerimento deve ser preenchido
       

    return render_to_response('portaria23/consulta.html',{'lista':p_extrato}, context_instance = RequestContext(request))

@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def emissao(request,id):
    #remove todos os registros para teste
    #calculotitulo = Tbcalculotitulo.objects.all().delete()
            
    global principal_corrigido_multa
    
    principal_corrigido_multa = 0
    instance = get_object_or_404(Tbextrato, id=id)
    modulos = instance.tamanho_modulos_fiscais
    vencimento = instance.data_vencimento_primeira_prestacao
    municipio = Tbmunicipio.objects.all()
    hoje = date.today()
    prestacao = float(instance.valor_imovel)/17.0
    titulado = vencimento.replace(vencimento.year - 3)
    area = instance.area_medida
    valor_imovel = instance.valor_imovel.quantize(Decimal('1.00'))
    dtrequerimento = None
    #icorrecao = 3.7779 #mudar para indice correto
    
    print "metodo ",request.method
    print "iten",request.POST
    #isenta pagamento para imoveis abaixo de 1 modulos fiscais'''
    isento = False
    ijuros = 0.0
    if modulos < 1:
        isento = True
    #definicao de qual taxa de juros vai utilizar    
    elif modulos > 4:
        ijuros = 6.75
    else:
        if valor_imovel <= 40000:
            ijuros = 1.0
        else: 
            if valor_imovel > 40000 and valor_imovel <= 100000:
                ijuros = 2.0
            else: 
                if valor_imovel > 100000:
                    ijuros = 4.0

    if request.method == "GET":
        if modulos > 1:
            messages.add_message(request, messages.INFO, 'O campo data de requerimento deve ser preenchido com a data que o titulado requereu formalmente o calculo')
    imulta = 1.0
    multa = 0 
    juros = 0 
    desconto = 0
        
    if request.method == "POST":
        if validar(request):
            dtrequerimento = datetime.datetime.strptime( request.POST['dtrequerimento'],'%d/%m/%Y')
            dtrequerimento = dtrequerimento.date()
        
        stNossaEscola = False
        if request.POST.get('stNossaEscola',False):
            stNossaEscola = True
        #ijuros = request.POST['ijuros'].replace(',','.')

        #icorrecao =  3.7779#request.POST['icorrecao'].replace(',','.')
        
        #verifica se existem GRUs geradas para o processo em questao
        calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__numero_processo__icontains = instance.numero_processo).order_by('parcela')
        
    pdf = []

    if dtrequerimento:
        if calculotitulo: 
            #se existir, montar uma lista que passe para o template o objeto calculotitulo e um flag para controlar se 
            #gera ou nao a referida GRU de cada parcela
            for obj in calculotitulo:
                #verificar se parcela estah vencida e gerar as correcoes , multas e juros
                verifica = verificavencimento(request,dtrequerimento,vencimento,ijuros,prestacao,titulado,obj,obj.parcela,imulta,stNossaEscola,instance)
                #se estiver paga,nao gerar nova gru pois senao vai sobrepor o calculo
                print "obj.stpaga",obj.stpaga, "obj.stgerada",obj.stgerada,"verifica['stgerada'] ",verifica['stgerada']
                if obj.stpaga == True or obj.stgerada == True:
                    print "gerada ou paga"
                    pass
                else:
                    #desconto para essa parcela a referida, atualiza as parcelas apartir da nova data de requerimento
                    #verificar modo de poder gerar novas parcelas sob demanda apartir de datas de requerimento atualizada
                    #pelo usuario
                    f_calculotitulo = Tbcalculotitulo(
                                    tbextrato = Tbextrato.objects.get(id = instance.id),
                                    parcela = obj.parcela,
                                    cdrecolhimento = obj.cdrecolhimento,
                                    nrreferencia = obj.nrreferencia,
                                    dtvencimento = obj.dtvencimento,
                                    cdug = obj.cdug,
                                    vlprincipal = prestacao,
                                    vldesconto = verifica['desconto'],
                                    vldeducoes = 0,
                                    vlmulta = multa,
                                    vljuros = verifica['juros'],
                                    vlcorrecao = verifica['correcao'],
                                    vlacrescimos = 0, 
                                    vltotal = verifica['principal_corrigido'],
                                    auth_user = obj.auth_user,
                                    created_at = obj.created_at,
                                    stpaga  = obj.stpaga,
                                    stgerada = verifica['stgerada'],
                                    id = obj.id,
                                    )
                    f_calculotitulo.save() 

                    pdf.append(verifica['data'])
        else:
            #tem que criar os 17 registros iniciais de gru. serao marcadas como nao pagas, nao emitidas 
            #gerar tambem uma lista que passe para o template o objeto calculotitulo e um flag para controlar se 
            #gera ou nao a referida GRU de cada parcela 
            for i in range(1,10):
                verifica = verificavencimento(request,dtrequerimento,vencimento,ijuros,prestacao,titulado,None,i,imulta,stNossaEscola,instance)
                f_calculotitulo = Tbcalculotitulo(
                                tbextrato = Tbextrato.objects.get(id = instance.id),
                                parcela = i,
                                cdrecolhimento = "28874-8",
                                nrreferencia = verifica['referencia'],
                                dtvencimento = vencimento, 
                                cdug = "373001/37201",#definir qual serah a UG do terra
                                vlprincipal = prestacao,
                                vldesconto = verifica['desconto'],
                                vldeducoes = 0,
                                vlmulta = verifica['multa'],
                                vlcorrecao = verifica['correcao'],
                                vljuros = verifica['juros'],
                                vlacrescimos = 0, 
                                vltotal = verifica['principal_corrigido'],
                                auth_user = AuthUser.objects.get( pk = request.user.id ),
                                stpaga  = False,
                                stgerada = False,
                                )
                f_calculotitulo.save()

                vencimento = vencimento.replace(vencimento.year + 1)

    titulado = formatDataToText(titulado)
    prestacao = "{0:.2f}".format(prestacao)
    desconto = "{0:.2f}".format(desconto)
    multa = "{0:.2f}".format(multa)
    ordem = 1
    
    dtrequerimento = formatDataToText(dtrequerimento)
    dtRequerimentoArq = dtrequerimento.replace('/','_')
    print "dtRequerimentoArq",dtRequerimentoArq
    
    calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__id = instance.id).order_by('parcela')

    print"------------------------"    
    
    #copiei para gerar gru
    if request.method == "POST":
        # Render html content through html template with context
        for obj in pdf:
            if obj <> None:
                print "pdf 1",obj
                template = get_template('portaria23/testePDF.html')
                html  = template.render(Context(obj))

                # Write PDF to file
                print"antes file"
                #file = open(os.path.join(settings.MEDIA_ROOT, 'teste'+dtRequerimentoArq+'.pdf'), "w+b")
                #pisaStatus = pisa.CreatePDF(html, dest=file,
                #        link_callback = link_callback)
                print "apos",file
                # Return PDF document through a Django HTTP response
                #file.seek(0)
                #pdf = file.read()
                #file.close()            # Don't forget to close the file handle
                #return HttpResponse(pdf, mimetype='application/pdf')
                return HttpResponse(html)
    #ateh aqui
    return render_to_response('portaria23/calculo.html' ,locals(), context_instance = RequestContext(request))


    
@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def digitar(request):
        
    return render_to_response('portaria23/calculo.html' ,locals(), context_instance = RequestContext(request))

def verificavencimento(request,dtrequerimento,dtvencimento,ijuros,prestacao,titulado,obj,numero_parcela,imulta,stNossaEscola,instance):
    #ijuros = float(request.POST.get('ijuros').replace(',','.'))
    #icorrecao = float(request.POST.get('icorrecao').replace(',','.'))
    correcao = 0
    principal = 0 
    principal_juros_correcao = 0
    multa = 0
    desconto = 0
    principal_corrigido_desconto = 0
    principal_corrigido_multa = 0
    dtgeracao = None
    stgerada =False
    data = None
    print "------------- PARCELA -----------",numero_parcela
    
    if dtrequerimento < dtvencimento: # nao vencido
        print "nao vencido"
        if (dtvencimento - dtrequerimento).days < 30:
            #incide juros de emissao titulo ateh vencimento parcela
            dias_juros = (dtvencimento - titulado).days
            dtvencGRU = dtvencimento
            print "dias_juros ",(dias_juros)
            juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
            prestacao_juros = prestacao + juros
            principal_corrigido = prestacao_juros
            imprime(prestacao_juros,"prestacao_juros")
            
        else:
            if (dtvencimento - dtrequerimento).days > 30:
                print "nao vencido - mais de 30 dias"   
                #incide juros de emissao titulo ate dtrequerimento + 30 dias
                dias_juros = (dtrequerimento - titulado).days + 30
                dtvencGRU = dtrequerimento + timedelta(30)
                juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
                prestacao_juros = prestacao + juros
                principal_corrigido = prestacao_juros
                
                imprime(prestacao_juros,"prestacao_juros")
                print "dias_juros " ,dias_juros,"prestacao ",prestacao," ijuros ",ijuros
                print "juros ",juros            
    else:
        if dtrequerimento > dtvencimento: # vencido
            print"vencido "
            print"prestacao" ,prestacao
            #incide multa,correcao (a partir do dtVencParcela ) e juros (apartir de dtEmissaoTitulo)
            # juros de emissao ateh dtrequerimento + 30 dias - incidencia aa
            dias_juros = (dtrequerimento - titulado).days + 30
            dtvencGRU = dtrequerimento + timedelta(30)
            juros = float(prestacao)*((float(dias_juros)/360.)*(ijuros/100.0))
            print "juros ",juros
            prestacao_juros = prestacao + juros
            print "prestacao_juros",prestacao_juros            

            # correcao de vencimento ate dtrequerimento + 30 dias
            # falta obter a correcao correta a ser aplicada de acordo com tabela do governo
            dias_correcao = (dtrequerimento - dtvencimento).days + 30
            
            #calcular a correcao: TbtrMensal
            icorrecao = 3.7779

            correcao = prestacao_juros*((icorrecao/100.0))
            print"correcao",correcao
            print "icorrecao",icorrecao
            principal_juros_correcao = prestacao_juros + correcao
            

            # multa de vencimento ateh dtrequerimento + 30 dias
            multa = ((float(dias_correcao))/30)*float(imulta)/100*float(principal_juros_correcao)  
            principal_corrigido = principal_juros_correcao + multa
            
            print "principal_corrigido ", principal_corrigido
            print "dtvencGRU ",dtvencGRU
            print "multa",multa
    referencia = str(instance.numero_processo[0:5])+str(instance.id_req[2:6])+str(numero_parcela)+str(0) #mudar qdo titulo vier do sisterleg
    if stNossaEscola:
        desconto = principal_corrigido / 2
        principal_corrigido = desconto

    #copiei para gerarGRU
    if obj is not None:
        if request.POST.get(str(obj.id)+'-parcela', False):
                #a parcela que forem marcadas devem ser geradas GRU caso nao tenham sido pagas 
                print "parcela"+ str(obj.parcela)+" marcou. Pago = " + str(obj.stpaga)
                dtgeracao = datetime.date.today()
                stgerada = True
                #cria um json para passar para o template que vai exibir a GRU
                data = {}
                data['recolhimento'] = "28874-8"
                data['prestacao'] = "{0:.2f}".format(prestacao)
                data['cpf'] = instance.cpf_req
                data['cdug'] = obj.cdug
                data['nome'] = instance.nome_req
                data['vencimento'] = dtvencimento
                data['referencia'] = referencia
                data['desconto'] = "{0:.2f}".format(desconto)
                data['multa'] = "{0:.2f}".format(multa)
                data['juros'] = "{0:.2f}".format(juros)
                data['total'] = "{0:.2f}".format(principal_corrigido)
                data['gerada'] = stgerada
                #messages.add_message(request,messages.WARNING,'GRU GERADA')
        else:
            #parcelas nao marcadas
            print "parcela"+ str(obj.parcela)+" nao marcou. Pago = " + str(obj.stpaga)

    #ateh aqui
    return locals()

def validar(request):
    warning = True
    if request.POST.get('icorrecao') == "":
        messages.add_message(request,messages.WARNING,'Informe um indice de correcao a ser aplicado')
        warning = False

    if request.POST.get('dtrequerimento') == "":
        messages.add_message(request, messages.INFO, 'O campo data de requerimento deve ser preenchido com a data que o titulado requereu formalmente o calculo')
        warning = False
    
    return warning

def imprime(valor,nome):
    print nome + str(valor) + str(type(valor))
    return

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
# remover !!!!!!!!!!!!!!!!!!!!!!
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

def geraPDF(request,data):

    data = {}
    data['recolhimento'] = "28874-8"
    data['farmer'] = 'Old MacDonald'
    data['animals'] = [('Cow', 'Moo'), ('Goat', 'Baa'), ('Pig', 'Oink')]
    
    # Render html content through html template with context
    t = loader.get_template('portaria23/testePDF.html')
    c = Context(data)
    html =  t.render(c)
    return HttpResponse(html)
    print "depois do template"

    #html  = template.render(Context(data))
    # Write PDF to file
    file = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=file,
            link_callback = link_callback)

    # Return PDF document through a Django HTTP response
    file.seek(0)
    pdf = file.read()
    file.close()            # Don't forget to close the file handle
    print "antes do HttpResponse"
    return HttpResponse(pdf, mimetype='application/pdf')

#USAR esta view para poder dividir o codigo e usar o botao GERAR GRU para ser direcionado para ca
def geraGRU(request,id):
    print "geraGRU id",id
    instance = get_object_or_404(Tbextrato, id=id)
    calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__numero_processo__icontains = instance.numero_processo).order_by('parcela')
    
    calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__id = instance.id).order_by('parcela')
    
    pdf = []

#    print "metodo", HttpRequest.method
#    print HttpRequest.path
#    print 'Parcela: '+request.POST['258-parcela']     

    if calculotitulo:
        for obj in calculotitulo:
            if request.POST.get(str(obj.id)+'-parcela', False):
                #a parcela que forem marcadas devem ser geradas GRU caso nao tenham sido pagas 
                print "parcela"+ str(obj.parcela)+" marcou. Pago = " + str(obj.stpaga)
                dtgeracao = datetime.date.today()
                stgerada = True
                #cria um json para passar para o template que vai exibir a GRU
                data = {}
                data['recolhimento'] = "28874-8"
                #data['prestacao'] = "{0:.2f}".format(prestacao)
                data['cpf'] = instance.cpf_req
                data['cdug'] = obj.cdug
                data['nome'] = instance.nome_req
                #data['vencimento'] = dtvencimento
                #data['referencia'] = referencia
                #data['desconto'] = "{0:.2f}".format(desconto)
                #data['multa'] = "{0:.2f}".format(multa)
                #data['juros'] = "{0:.2f}".format(juros)
                #data['total'] = "{0:.2f}".format(principal_corrigido)
                data['gerada'] = stgerada
                pdf.append(['data'])
            else:
                #parcelas nao marcadas
                print "parcela"+ str(obj.parcela)+" nao marcou. Pago = " + str(obj.stpaga)

    # Render html content through html template with context
    for obj in pdf:
        if obj <> None:
            print "pdf 1",obj
            #template = get_template('portaria23/testePDF.html')
            #html  = template.render(Context(obj))

            # Write PDF to file
            print"antes file"
            #file = open(os.path.join(settings.MEDIA_ROOT, 'teste'+dtRequerimentoArq+'.pdf'), "w+b")
            #pisaStatus = pisa.CreatePDF(html, dest=file,
            #        link_callback = link_callback)
            print "apos",file
            # Return PDF document through a Django HTTP response
            #file.seek(0)
            #pdf = file.read()
            #file.close()            # Don't forget to close the file handle
            #return HttpResponse(pdf, mimetype='application/pdf')
            #return HttpResponse(html)
            return render_to_response('portaria23/testePDF.html' ,
                {
                    'nome':instance.nome_req,
                    'cpf':instance.cpf_req
                }, 
                context_instance = RequestContext(request))

    return render_to_response('portaria23/calculo.html' ,locals(), context_instance = RequestContext(request))
   