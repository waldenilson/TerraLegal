from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from TerraLegal.calculo.models import Tbextrato, Tbcalculotitulo
from TerraLegal.tramitacao.models import Tbmunicipio, AuthUser
from decimal import Decimal
from datetime import date
from TerraLegal.tramitacao.restrito.processo import formatDataToText
from django.contrib import messages
import datetime
from datetime import timedelta
import time



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
    calculotitulo = Tbcalculotitulo.objects.all().delete()
            
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
    icorrecao = 3.7779 #mudar para indice correto
    
    #isenta pagamento para imoveis abaixo de 1 modulos fiscais'''
    isento = False
    if modulos < 1:
        isento = True

    #definicao de qual taxa de juros vai utilizar    
    if modulos > 4:
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
        

        #verifica se existem GRUs geradas para o processo em questao
        calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__numero_processo__icontains = instance.numero_processo).order_by('parcela')
        for obj in calculotitulo:
            if request.POST.get(str(obj.id)+'-parcela', False):
                #as parcelas que forem marcadas devem ser geradas GRU caso nao tenham sido pagas 
                print "parcela"+ str(obj.parcela)+" marcou. estava " + str(obj.stpaga)
            else:
                #parcelas nao marcadas
                print "parcela"+ str(obj.parcela)+" nao marcou. estava " + str(obj.stpaga)
    
    if dtrequerimento:
        if calculotitulo: 
            #se existir, montar uma lista que passe para o template o objeto calculotitulo e um flag para controlar se 
            #gera ou nao a referida GRU de cada parcela
            for obj in calculotitulo:
                print "aqui 1"
                #verificar se parcela estah vencida e gerar as correcoes , multas e juros
                verifica = verificavencimento(request,dtrequerimento,vencimento,ijuros,prestacao,titulado,obj,None,imulta,stNossaEscola)
                #se estiver paga nao gerar nova gru pois senao vai sobrepor o calculo
                if obj.stpaga == True and obj.stgerada == True:
                    pass
                else:
                    #desconto para essa parcela a referida 
                    f_calculotitulo = Tbcalculotitulo(
                                    tbextrato = Tbextrato.objects.get(id = instance.id),
                                    parcela = obj.parcela,
                                    cdrecolhimento = obj.cdrecolhimento,
                                    nrreferencia = obj.nrreferencia,
                                    dtvencimento = obj.dtvencimento,
                                    cdug = "TESTE2", #obj.cdug,
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
                                    id = obj.id,
                                    )
                    f_calculotitulo.save()         
        else:
            #tem que criar os 17 registros iniciais de gru. serao marcadas como nao pagas, nao emitidas 
            #gerar tambem uma lista que passe para o template o objeto calculotitulo e um flag para controlar se 
            #gera ou nao a referida GRU de cada parcela 
            for i in range(1,18):
                print "cria parcelas"
                verifica = verificavencimento(request,dtrequerimento,vencimento,ijuros,prestacao,titulado,None,i,imulta,stNossaEscola)
                f_calculotitulo = Tbcalculotitulo(
                                tbextrato = Tbextrato.objects.get(id = instance.id),
                                parcela = i,
                                cdrecolhimento = "28874-8",
                                nrreferencia = str(instance.numero_processo[0:5])+str(instance.id_req[2:6])+str()+"0", #mudar quando o titulo vier do sisterleg
                                dtvencimento = vencimento, 
                                cdug = "373001/37201",
                                vlprincipal = prestacao,
                                vldesconto = verifica['desconto'],
                                vldeducoes = 0,
                                vlmulta = verifica['multa'],
                                vlcorrecao = verifica['correcao'],
                                vljuros = verifica['juros'],
                                vlacrescimos = 0, 
                                vltotal = verifica['principal_corrigido'],
                                auth_user = AuthUser.objects.get( pk = request.user.id ),
                                stpaga  = False
                                )
                f_calculotitulo.save()
                vencimento = vencimento.replace(vencimento.year + 1)

    titulado = formatDataToText(titulado)
    prestacao = "{0:.2f}".format(prestacao)
    desconto = "{0:.2f}".format(desconto)
    multa = "{0:.2f}".format(multa)
    ordem = 1
    
    dtrequerimento = formatDataToText(dtrequerimento)

    print "dtrequerimento " + str(dtrequerimento) + str(type(dtrequerimento))

    
    calculotitulo = Tbcalculotitulo.objects.all().filter(tbextrato__id = instance.id).order_by('parcela')
    return render_to_response('portaria23/calculo.html' ,locals(), context_instance = RequestContext(request))


@permission_required('sicop.titulo_calculo_portaria23', login_url='/excecoes/permissao_negada/', raise_exception=True)
def digitar(request):
        
    return render_to_response('portaria23/calculo.html' ,locals(), context_instance = RequestContext(request))

def verificavencimento(request,dtrequerimento,dtvencimento,ijuros,prestacao,titulado,obj,numero_parcela,imulta,stNossaEscola):
    ijuros = float(request.POST.get('ijuros').replace(',','.'))
    icorrecao = float(request.POST.get('icorrecao').replace(',','.'))
    correcao = 0
    principal = 0 
    principal_juros_correcao = 0
    multa = 0
    desconto = 0
    principal_corrigido_desconto = 0
    principal_corrigido_multa = 0
    print "--------------PARCELA-----------",numero_parcela
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
    
    if stNossaEscola:
        desconto = principal_corrigido / 2
        principal_corrigido = desconto

    return locals()

def validar(request):
    print "validar"
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
