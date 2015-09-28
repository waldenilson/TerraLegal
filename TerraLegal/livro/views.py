from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from TerraLegal.livro.models import Tbtitulo, Tbstatustitulo, Tbtipotitulo , Tbtituloprocesso
from TerraLegal.tramitacao.models import AuthUser, Tbprocessobase, Tbprocessorural,Tbdivisao, Tbpecastecnicas, Tbcaixa
from django.http import HttpResponseRedirect
from django.contrib import messages
from TerraLegal.tramitacao.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from django.http.response import HttpResponse
from odslib import ODS
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from os.path import abspath, join, dirname
from TerraLegal.core.funcoes import upload_file


nome_relatorio      = "relatorio_livro"
processos_relatorio = "dados_processos_relatorio"
response_consulta   = "/livro/consulta/"
titulo_relatorio    = "Relatorio Livro Fundiario"
planilha_relatorio  = "Livro Fundiario"

#view com acesso a livro fundiario diretamente na tabela sem uso de form. Verificar
#como feito o html para acessar as FK. Nao usa form. Faz validacao apos o submit da edicao.
@permission_required('sicop.livro_carga', login_url='/excecoes/permissao_negada/', raise_exception=True)
def carga(request):
    filename = settings.CSV_PATH_DIR + '/livro_fundioario.csv'
    flivro = csv.DictReader(open(filename,"rb"),delimiter=',')
    l_flivro = []
    for line in flivro:
        l_flivro.append(line)

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    request.session['nome_relatorio'] = []
    caixa = []
    for obj in Tbcaixa.objects.all().filter(tbdivisao__id = AuthUser.objects.get(pk = request.user.id ).tbdivisao.id):
        if obj.tbtipocaixa.nmtipocaixa=='TIT':
            caixa.append(obj)

    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        #por enquanto lista somente processo rural. se for colocar convenio alterar aqui
        lista_processo = Tbprocessorural.objects.all().filter(tbprocessobase__tbtituloprocesso__tbtitulo__cdtitulo__icontains=cdtitulo,
                                                     tbprocessobase__nrprocesso__icontains=nrprocesso,
                                                     nrcpfrequerente__icontains = cpf,
                                                     nmrequerente__icontains = requerente)
        lista_processo = lista_processo.order_by('tbprocessobase.nrprocesso')
        lista = []
        for obj in lista_processo:
            lista.append (Tbtituloprocesso.objects.get(tbtitulo__cdtitulo__icontains=cdtitulo,
                                                                tbprocessobase__id = obj.tbprocessobase.id))
        
        lista_titulo = Tbtitulo.objects.all().filter(cdtitulo__icontains=cdtitulo)
        

        request.session['nome_relatorio'] = lista

        return render_to_response('livro/consulta.html' ,{'lista':lista,'lista_titulo':lista_titulo,
                        'lista_processo':lista_processo}, context_instance = RequestContext(request))
    return render_to_response('livro/consulta.html',context_instance = RequestContext(request))

@permission_required('sicop.livro_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    response_consulta  = "/livro/consulta/"
    caixa = []
    for obj in Tbcaixa.objects.all().filter(tbdivisao__id = AuthUser.objects.get(pk = request.user.id ).tbdivisao.id):
        if obj.tbtipocaixa.nmtipocaixa=='TIT':
            caixa.append(obj)

    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validarProcesso(request,'cadastro'):
            processobase = Tbprocessobase.objects.get( nrprocesso = request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
            #titulo = Tbtitulo.objects.get(cdtitulo = request.POST['cdtitulo'])
            #cria o registro do titulo caso ele nao exista
            try:
                titulo = Tbtitulo.objects.get(  
                    cdtitulo = request.POST['cdtitulo'],
                    tbtipotitulo = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo'])            )
            except ObjectDoesNotExist:
                f_titulo = Tbtitulo(
                            cdtitulo        = request.POST['cdtitulo'],
                            tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                            tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo']),
                            auth_user       = AuthUser.objects.get( pk = request.user.id ),
                            tbcaixa         = Tbcaixa.objects.get (pk = request.POST['tbcaixa'])
                            
                        )
                f_titulo.save()
                titulo = Tbtitulo.objects.get(pk=f_titulo.id)
            
            #associa o titulo ao processo
            f_tituloprocesso = Tbtituloprocesso(
                        tbprocessobase = Tbprocessobase.objects.get(id = processobase.id),        
                        tbtitulo = Tbtitulo.objects.get(id = titulo.id),
                        auth_user = AuthUser.objects.get( pk = request.user.id )
                        )
            f_tituloprocesso.save()
            
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
        else: # deu erro no cadastro, retornar a tela com os dados preenchidos  
            return render_to_response('livro/cadastro.html',
                {"statustitulo":statustitulo,"tipotitulo":tipotitulo,"caixa":caixa},context_instance = RequestContext(request))           

    return render_to_response('livro/cadastro.html',{"statustitulo":statustitulo,"tipotitulo":tipotitulo,"caixa":caixa}
                            , context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):#id eh da relacao tituloprocesso
    caixa = []
    for obj in Tbcaixa.objects.all().filter(tbdivisao__id = AuthUser.objects.get(pk = request.user.id ).tbdivisao.id):
        if obj.tbtipocaixa.nmtipocaixa=='TIT':
            caixa.append(obj)

    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()

    tituloprocesso = Tbtituloprocesso.objects.get(id = id)
    rural = Tbprocessorural.objects.get(tbprocessobase__id = tituloprocesso.tbprocessobase.id)
    processobase = Tbprocessobase.objects.get(pk = tituloprocesso.tbprocessobase.id)
    titulo = Tbtitulo.objects.get(pk = tituloprocesso.tbtitulo.id)
    
    peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente)
    
    
    if request.method == "POST":
        
        arquivo_digital = 0

        if not request.user.has_perm('sicop.livro_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/')
        
        if validarProcesso(request,'edicao'):
            processobase_novo = Tbprocessobase.objects.get(nrprocesso=request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
            rural_novo = Tbprocessorural.objects.get(tbprocessobase__nrprocesso=processobase_novo.nrprocesso)
            
            #upload do titulo pdf
            if request.FILES:
                arquivo_digital = upload_file(
                    request.FILES['arquivo_digital'],
                    abspath(join(dirname(__file__), '../../media'))+'/doc/upload/titulacao/'+AuthUser.objects.get( pk = request.user.id ).tbdivisao.tbuf.sigla+'/P23/'+request.POST['cdtitulo']+'.pdf',
                    request.FILES['arquivo_digital'].name,
                    'pdf'
                )

            #altera os dados do titulo
            f_titulo = Tbtitulo(
                cdtitulo = request.POST['cdtitulo'],
                tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo']),  
                tbcaixa = Tbcaixa.objects.get(id = request.POST['tbcaixa']),
                id = titulo.id
                )

            if int(arquivo_digital) == 1:
                print arquivo_digital
                f_titulo.path_file = '/media/doc/upload/titulacao/MA/P23/'+f_titulo.cdtitulo+'.pdf'
            f_titulo.save()
            #verifica se usuario digitou processo para alterar o titulo
            if processobase.nrprocesso <> processobase_novo.nrprocesso:
                #se o titulo nao existir, cria o registro do titulo
                #verifica se o titulo existe
                try:
                    titulo = Tbtitulo.objects.get(  
                        cdtitulo = request.POST['cdtitulo'],
                        tbtipotitulo = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo'])
                        )
                except ObjectDoesNotExist:
                    f_titulo = Tbtitulo(
                                cdtitulo        = request.POST['cdtitulo'],
                                tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                                tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo']),
                                auth_user       = AuthUser.objects.get( pk = request.user.id ),
                                tbcaixa         = Tbcaixa.objects.get (pk = request.POST['tbcaixa'])
                                 )
                    if arquivo_digital == 1:
                        f_titulo.path_file = '/media/doc/upload/titulacao/MA/P23/'+f_titulo.cdtitulo+'.pdf'
                    f_titulo.save()
                    titulo = Tbtitulo.objects.get(id = f_titulo.id)
                #associa o titulo jah existente ao processo digitado
                f_tituloprocesso = Tbtituloprocesso(
                            id = tituloprocesso.id,
                            tbprocessobase = Tbprocessobase.objects.get(pk = processobase_novo.id),
                            tbtitulo = Tbtitulo.objects.get(pk = titulo.id),
                            auth_user = AuthUser.objects.get( pk = request.user.id),
                            created_at = tituloprocesso.created_at

                            )
                f_tituloprocesso.save()
                tituloprocesso = Tbtituloprocesso.objects.get(pk = f_tituloprocesso.id)
            
            return HttpResponseRedirect("/livro/edicao/"+str(tituloprocesso.id)+"/")
    else: #nao eh POST
        tituloprocesso = Tbtituloprocesso.objects.get(id = id)
        rural = Tbprocessorural.objects.get(tbprocessobase__id = tituloprocesso.tbprocessobase.id)
        processobase = Tbprocessobase.objects.get(pk = tituloprocesso.tbprocessobase.id)
        titulo = Tbtitulo.objects.get(pk=tituloprocesso.tbtitulo.id)
        peca = Tbpecastecnicas.objects.all().filter(nrcpfrequerente = rural.nrcpfrequerente)
        
        if processobase.tbdivisao.id <> AuthUser.objects.get(pk = request.user.id).tbdivisao.id:
            return HttpResponseRedirect('/excecoes/permissao_negada/')
     

    return render_to_response('livro/edicao.html', {"titulo":titulo,"statustitulo":statustitulo,"tipotitulo":tipotitulo,
                                                    "processo":processobase,"peca":peca,"rural":rural,
                                                    "tituloprocesso":tituloprocesso,"caixa":caixa}, 
                                                    context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def titulos_entregues(request):
    global nome_relatorio    
    global response_consulta  
    global titulo_relatorio   
    global planilha_relatorio 
    global processos_relatorio


    nome_relatorio      = "relatorio_livro_entregues"
    processos_relatorio = "dados_processos_relatorio"
    response_consulta  = "/livro/consulta_entregues/"
    titulo_relatorio    = "Relatorio Livro Fundiario - Titulos entregues"
    planilha_relatorio  = "Livro Fundiario - Entregues"


    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        
        lista = Tbtituloprocesso.objects.all().filter(tbtitulo__cdtitulo__icontains=cdtitulo,
                                tbprocessobase__nrprocesso__icontains=nrprocesso,
                                tbtitulo__tbstatustitulo__id__exact = 1
                                )
        lista = lista.order_by( 'tbtitulo.cdtitulo' )
        lista_processo = []
        for obj in lista:
            lista_processo.append (Tbprocessorural.objects.get(
                                tbprocessobase__id=obj.tbprocessobase.id,
                                nrcpfrequerente__icontains= cpf,
                                nmrequerente__icontains= requerente))
    else:
        lista = Tbtituloprocesso.objects.all().filter(tbtitulo__tbstatustitulo__id__exact = 1)
        lista_processo = []
        lista = lista.order_by( 'tbtitulo.cdtitulo' )
        for obj in lista:
            lista_processo.append (Tbprocessorural.objects.get(tbprocessobase__id__icontains = obj.tbprocessobase.id))
       
    request.session[nome_relatorio] = lista
    request.session[processos_relatorio] = lista_processo

    return render_to_response('livro/consulta_entregues.html' ,{'lista':lista,'lista_processo':lista_processo}, context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def titulos_nao_entregues(request):
    global nome_relatorio 
    global response_consulta  
    global titulo_relatorio   
    global planilha_relatorio 
    global processos_relatorio

    nome_relatorio      = "relatorio_livro_nao_entregues"
    processos_relatorio = "dados_processos_relatorio"
    response_consulta   = "/livro/consulta_nao_entregues/"
    titulo_relatorio    = "Relatorio Livro Fundiario - Titulos nao entregues"
    planilha_relatorio  = "Livro Fundiario - Nao entregues"

    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        
        lista = Tbtituloprocesso.objects.all().filter(tbtitulo__cdtitulo__icontains=cdtitulo,
                                tbprocessobase__nrprocesso__icontains=nrprocesso,
                                tbtitulo__tbstatustitulo__id__exact = 2
                                )
        lista = lista.order_by( 'tbtitulo.cdtitulo' )
        lista_processo = []
        for obj in lista:
            lista_processo.append (Tbprocessorural.objects.get(
                                tbprocessobase__id=obj.tbprocessobase.id,
                                nrcpfrequerente__icontains= cpf,
                                nmrequerente__icontains= requerente))
    else:
        lista = Tbtituloprocesso.objects.all().filter(tbtitulo__tbstatustitulo__id__exact = 2)
        lista = lista.order_by( 'tbtitulo.cdtitulo' )
        lista_processo = []
        for obj in lista:
            lista_processo.append (Tbprocessorural.objects.get(tbprocessobase__id__icontains = obj.tbprocessobase.id))
       
    request.session[nome_relatorio] = lista
    request.session[processos_relatorio] = lista_processo
    return render_to_response('livro/consulta_nao_entregues.html' ,{'lista':lista,'lista_processo':lista_processo}, context_instance = RequestContext(request))
    
@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):
    # montar objeto lista com os campos a mostrar no relatorio
    lista = request.session[nome_relatorio]
    lista_processo =  request.session[processos_relatorio]

    if lista:

        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(lista),  ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Titulo' ).setFontSize('10pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('10pt')
        sheet.getCell(2, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('10pt')
        sheet.getCell(3, 1).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('10pt')
        sheet.getCell(4, 1).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('10pt')
        sheet.getCell(5, 1).setAlignHorizontal('center').stringValue( 'Municipio do imovel' ).setFontSize('10pt')
        sheet.getCell(6, 1).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('10pt')
        sheet.getCell(7, 1).setAlignHorizontal('center').stringValue( 'CPF conjuge' ).setFontSize('10pt')
        sheet.getCell(8, 1).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('10pt')
        sheet.getCell(9, 1).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('10pt')
        sheet.getCell(10, 1).setAlignHorizontal('center').stringValue( 'Municipio domicilio' ).setFontSize('10pt')
        sheet.getCell(11, 1).setAlignHorizontal('center').stringValue( 'Pasta' ).setFontSize('10pt')
        
        
        sheet.getRow(1).setHeight('10pt')
        #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0,  x+3).setAlignHorizontal('left').stringValue(obj.tbtitulo.cdtitulo)
            sheet.getCell(1,  x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(4,  x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            sheet.getCell(5,  x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(8,  x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(9,  x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nmcontato)
            try:
                sheet.getCell(10, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbmunicipiodomicilio.nome_mun)
            except:
                sheet.getCell(10, x+3).setAlignHorizontal('left').stringValue('')
                
            try:
                sheet.getCell(11, x+3).setAlignHorizontal('left').stringValue(obj.tbtitulo.tbcaixa.nmlocalarquivo)
            except:
                sheet.getCell(11, x+3).setAlignHorizontal('left').stringValue('')
            
                 
            
            for obj2 in lista_processo:
                if obj.tbprocessobase.id == obj2.tbprocessobase.id:
                    sheet.getCell(2, x+3).setAlignHorizontal('left').stringValue(obj2.nmrequerente)
                    sheet.getCell(3, x+3).setAlignHorizontal('left').stringValue(obj2.nrcpfrequerente)
                    sheet.getCell(6, x+3).setAlignHorizontal('left').stringValue(obj2.nmconjuge)
                    sheet.getCell(7, x+3).setAlignHorizontal('left').stringValue(obj2.nrcpfconjuge)

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

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_pdf(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(mimetype='application/pdf')
        doc = relatorio_pdf_base_header(response, nome_relatorio)   
        elements=[]
        
        dados = relatorio_pdf_base_header_title(titulo_relatorio)
        dados.append( ('NOME','CAIXA') )
        for obj in lista:
            dados.append( ( obj.nmlocalarquivo , obj.tbtipocaixa.nmtipocaixa ) )
        return relatorio_pdf_base(response, doc, elements, dados)
    else:
        return HttpResponseRedirect(response_consulta)

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_csv(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        response = HttpResponse(content_type='text/csv')     
        writer = relatorio_csv_base(response, nome_relatorio)
        writer.writerow(['Nome', 'Tipo'])
        for obj in lista:
            writer.writerow([obj.nmlocalarquivo, obj.tbtipocaixa.nmtipocaixa])
        return response
    else:
        return HttpResponseRedirect( response_consulta )

def validacao(request_form):
    warning = True
    if request_form.POST['tbstatustitulo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um status para o titulo')
        warning = False
    if request_form.POST['tbtipotitulo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o tipo de titulo')
        warning = False
    return warning

def validarProcesso(request_form,acao):
    global fgexiste 
    global bltituloexiste

    base = request_form.POST['tbprocessobase'].replace('.','').replace('/','').replace('-','')
    warning = True


    #copiado edicao
    if request_form.POST['tbstatustitulo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe um status para o titulo')
        warning = False
        return warning
    if request_form.POST['tbtipotitulo'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o tipo de titulo')
        warning = False
        return warning
    #copiado edicao

    #verificar se processo existe
    try:
        processo = Tbprocessobase.objects.get(nrprocesso = base)
    except ObjectDoesNotExist:
        messages.add_message(request_form, messages.WARNING, 'O processo '+str(base)+' nao existe. Titulo nao cadastrado')
        warning = False
        return warning 
   
    #verifica se o titulo existe
    try:
        titulo = Tbtitulo.objects.get(  
            cdtitulo = request_form.POST['cdtitulo'],
            tbtipotitulo = Tbtipotitulo.objects.get(id = request_form.POST['tbtipotitulo'])
            )
    except ObjectDoesNotExist:
        bltituloexiste = False
        warning = True
    else:
        bltituloexiste = True 

    #verificar ser o titulo estah associado a algum processo. Pode ser que o titulo exista mas
    # nao tenha associao com tbtituloprocesso. Nao criar titulo. Criar associacao
    #se for cadastro, verificar  e nao permitir que se cadastre
    #se for edicao, deve permitir a alteracao, que serah uma nova associacao
    try:
        tituloprocesso = Tbtituloprocesso.objects.get(tbtitulo__cdtitulo = request_form.POST['cdtitulo'],
                                    tbtitulo__tbtipotitulo__id  = request_form.POST['tbtipotitulo'])
    except:
        warning = True
    else:
        if acao == 'cadastro':
            messages.add_message(request_form, messages.WARNING, 'O Titulo ' + request_form.POST['cdtitulo'] + 
                        ' ja associado ao processo '+ str(tituloprocesso.tbprocessobase.nrprocesso))
            warning = False
            return warning
        if acao == 'edicao':
            warning = True

    #aqui eh o contrario, verificar se o processo jah estah cadastrado com algum titulo
    try:
        tituloprocesso = Tbtituloprocesso.objects.get(tbprocessobase__nrprocesso = base)
    except:
        warning = True
    else:
        if acao == "cadastro":
            messages.add_message(request_form, messages.WARNING, 'O processo ' + base +  
                        ' ja associado ao titulo  '+ tituloprocesso.tbtitulo.cdtitulo)
            warning = False
            return warning
        if acao == 'edicao':
            warning = True          


    if processo:
        #verificar se o processo pertence a outra divisao
        divisao = Tbdivisao.objects.get(pk = Tbprocessobase.objects.get(nrprocesso = base).tbdivisao.id)
    
        if processo.tbdivisao.id != divisao.id:
            messages.add_message(request_form, messages.WARNING, 'O processo existe, mas pertence a outra divisao.')
            warning = False        
    
        #verifica se o processo base eh classificado como processo pai
        if processo.tbclassificacaoprocesso.id != 1:
            messages.add_message(request_form, messages.WARNING, 'Nao permitido associar tituloprocessotulo a  processo classificado como anexo/apenso.')
            warning = False        
        
        try:
            Tbtitulo.objects.get(tbprocessobase = processo.id) #this raises an ObjectDoesNotExist exception if it doesn't find a user with that username
        except ObjectDoesNotExist:
            warning = True   

    if request_form.POST['tbcaixa'] == '':  
        messages.add_message(request_form, messages.WARNING, 'Escolha a caixa ou pasta onde o titulo deve ser tramitado')
        warning = False

    return warning
