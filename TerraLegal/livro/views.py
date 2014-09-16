from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from TerraLegal.livro.models import Tbtitulo, Tbstatustitulo, Tbtipotitulo
from TerraLegal.tramitacao.models import AuthUser, Tbprocessobase, Tbprocessorural,Tbdivisao, Tbpecastecnicas
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

from TerraLegal import settings

nome_relatorio      = "relatorio_livro"
response_consulta  = "/livro/consulta/"
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
    
    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        #lista = Tbtitulo.objects.all().filter( cdtitulo__icontains=cdtitulo,tbprocessobase__nrprocesso__icontains=nrprocesso )
        lista = Tbprocessorural.objects.all().filter(tbprocessobase__tbtitulo__cdtitulo__icontains=cdtitulo,
                                                     tbprocessobase__nrprocesso__icontains=nrprocesso,
                                                     nrcpfrequerente__icontains = cpf,
                                                     nmrequerente__icontains = requerente)
        lista = lista.order_by('tbprocessobase.nrprocesso')
        
        request.session[nome_relatorio] = lista
        return render_to_response('livro/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    return render_to_response('livro/consulta.html',context_instance = RequestContext(request))

@permission_required('sicop.livro_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    response_consulta  = "/livro/consulta/"

   
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validarProcesso(request):
            processobase = Tbprocessobase.objects.get( nrprocesso = 
                    request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
            #cria o registro do titulo
            f_titulo = Tbtitulo(
                            cdtitulo = request.POST['cdtitulo'],
                            tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                            tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo'])
                        )
            f_titulo.save()
            titulo = Tbtitulo.objects.get(pk=f_titulo.id)
            #associa o titulo ao processo
            f_processobase = Tbprocessobase(
                        id = processobase.id,
                        nrprocesso = processobase.nrprocesso,
                        tbgleba = processobase.tbgleba,
                        tbmunicipio = processobase.tbmunicipio,
                        tbcaixa = processobase.tbcaixa,
                        tbtipoprocesso = processobase.tbtipoprocesso,
                        tbsituacaoprocesso = processobase.tbsituacaoprocesso,
                        dtcadastrosistema = processobase.dtcadastrosistema,
                        auth_user = AuthUser.objects.get( pk = request.user.id ),
                        tbdivisao = processobase.tbdivisao,
                        tbclassificacaoprocesso = processobase.tbclassificacaoprocesso,
                        nmendereco = processobase.nmendereco,
                        nmcontato = processobase.nmcontato,
                        tbtitulo = Tbtitulo.objects.get(pk=f_titulo.id),
                        tbmunicipiodomicilio = processobase.tbmunicipiodomicilio
                        
                        )
            f_processobase.save()
            
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('livro/cadastro.html',{"statustitulo":statustitulo,"tipotitulo":tipotitulo}, context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):#id eh do processo rural
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    
    if request.method == "POST":
        #titulo = get_object_or_404(Tbtitulo, id=id)
        if not request.user.has_perm('sicop.livro_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/')
        #processobase = Tbprocessobase.objects.get( nrprocesso = 
        #            request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
        
        rural = Tbprocessorural.objects.get(pk = id)
        processobase = Tbprocessobase.objects.get(pk = rural.tbprocessobase.id)
        processobase_novo = Tbprocessobase.objects.get(nrprocesso=request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
        rural_novo = Tbprocessorural.objects.get(tbprocessobase__nrprocesso=processobase_novo.nrprocesso)
        titulo = Tbtitulo.objects.get(pk = processobase.tbtitulo.id)
        
        if validacao(request):
            #rural = Tbprocessorural.objects.get( tbprocessobase = processobase.id)
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente)
            #altera os dados do titulo
            f_titulo = Tbtitulo(
                cdtitulo = request.POST['cdtitulo'],
                tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo']),  
                id = titulo.id
                )
            f_titulo.save()
            #verifica se usuario digitou processo para alterar o titulo
            if processobase.nrprocesso <> processobase_novo.nrprocesso:
                #associa o titulo ao processo digitado
                f_processobase = Tbprocessobase(
                            id = processobase_novo.id,
                            nrprocesso = processobase_novo.nrprocesso,
                            tbgleba = processobase_novo.tbgleba,
                            tbmunicipio = processobase_novo.tbmunicipio,
                            tbcaixa = processobase_novo.tbcaixa,
                            tbtipoprocesso = processobase_novo.tbtipoprocesso,
                            tbsituacaoprocesso = processobase_novo.tbsituacaoprocesso,
                            dtcadastrosistema = processobase_novo.dtcadastrosistema,
                            auth_user = processobase_novo.auth_user,
                            tbdivisao = processobase_novo.tbdivisao,
                            tbclassificacaoprocesso = processobase_novo.tbclassificacaoprocesso,
                            nmendereco = processobase_novo.nmendereco,
                            nmcontato = processobase_novo.nmcontato,
                            tbtitulo = Tbtitulo.objects.get(pk=f_titulo.id),
                            tbmunicipiodomicilio = processobase_novo.tbmunicipiodomicilio
                            )
                f_processobase.save()
                
                #desassocia o titulo pesquisado do processo
                f_processobase = Tbprocessobase(
                            id = processobase.id,
                            nrprocesso = processobase.nrprocesso,
                            tbgleba = processobase.tbgleba,
                            tbmunicipio = processobase.tbmunicipio,
                            tbcaixa = processobase.tbcaixa,
                            tbtipoprocesso = processobase.tbtipoprocesso,
                            tbsituacaoprocesso = processobase.tbsituacaoprocesso,
                            dtcadastrosistema = processobase.dtcadastrosistema,
                            auth_user = processobase.auth_user,
                            tbdivisao = processobase.tbdivisao,
                            tbclassificacaoprocesso = processobase.tbclassificacaoprocesso,
                            nmendereco = processobase.nmendereco,
                            nmcontato = processobase.nmcontato,
                            tbtitulo = None,
                            tbmunicipiodomicilio = processobase.tbmunicipiodomicilio,
                            )
                f_processobase.save()
            return HttpResponseRedirect("/livro/edicao/"+str(rural_novo.id)+"/")
    else:
        #titulo = get_object_or_404(Tbtitulo, id=id)
        #divisao = titulo.tbprocessobase.tbdivisao.id
        #processobase = get_object_or_404(Tbprocessobase, nrprocesso = titulo.tbprocessobase.nrprocesso)
        #rural = Tbprocessorural.objects.get( tbprocessobase = processobase.id)
        #peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente)
        #if divisao <> AuthUser.objects.get(pk = request.user.id).tbdivisao.id:
        #    return HttpResponseRedirect('/excecoes/permissao_negada/')
        rural = Tbprocessorural.objects.get(pk=id)
        processobase = Tbprocessobase.objects.get(pk=rural.tbprocessobase.id)
        titulo = Tbtitulo.objects.get(pk=processobase.tbtitulo.id)
        peca = Tbpecastecnicas.objects.all().filter(nrcpfrequerente = rural.nrcpfrequerente)
        if processobase.tbdivisao.id <> AuthUser.objects.get(pk = request.user.id).tbdivisao.id:
            return HttpResponseRedirect('/excecoes/permissao_negada/')
        
    return render_to_response('livro/edicao.html', {"titulo":titulo,"statustitulo":statustitulo,"tipotitulo":tipotitulo,"processo":processobase,"peca":peca,"rural":rural}, context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def titulos_entregues(request):
    global nome_relatorio     # = "relatorio_livro_entregues"
    global response_consulta  #= "/livro/consulta_entregues/"
    global titulo_relatorio   # = "Relatorio Livro Fundiario - Titulos entregues"
    global planilha_relatorio # = "Livro Fundiario - Entregues"
   
    nome_relatorio      = "relatorio_livro_entregues"
    response_consulta  = "/livro/consulta_entregues/"
    titulo_relatorio    = "Relatorio Livro Fundiario - Titulos entregues"
    planilha_relatorio  = "Livro Fundiario - Entregues"


    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        lista = Tbprocessorural.objects.all().filter( tbprocessobase__tbtitulo__cdtitulo__icontains=cdtitulo,
                                tbprocessobase__nrprocesso__icontains=nrprocesso,
                                nrcpfrequerente__icontains=cpf,nmrequerente__icontains=requerente,
                                tbprocessobase__tbtitulo__tbstatustitulo__id__exact = 1)
    else:
        lista = Tbprocessorural.objects.all().filter(tbprocessobase__tbtitulo__tbstatustitulo__id__exact = 1)
    #lista = lista.order_by('tbprocessobase.tbtitulo')
    request.session[nome_relatorio] = lista
    return render_to_response('livro/consulta_entregues.html' ,{'lista':lista}, context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def titulos_nao_entregues(request):
    global nome_relatorio #      = "relatorio_livro_nao_entregues"
    global response_consulta  #= "/livro/consulta_nao_entregues/"
    global titulo_relatorio   # = "Relatorio Livro Fundiario - Titulos nao entregues"
    global planilha_relatorio # = "Livro Fundiario - Nao entregues"

    nome_relatorio      = "relatorio_livro_nao_entregues"
    response_consulta   = "/livro/consulta_nao_entregues/"
    titulo_relatorio    = "Relatorio Livro Fundiario - Titulos nao entregues"
    planilha_relatorio  = "Livro Fundiario - Nao entregues"

    if request.method == "POST":
        cdtitulo = request.POST['cdtitulo']
        nrprocesso = request.POST['nrprocesso'].replace('.','').replace('/','').replace('-','')
        requerente = request.POST['nmrequerente']
        cpf = request.POST['nrcpfrequerente']
        lista = Tbprocessorural.objects.all().filter( tbprocessobase__tbtitulo__cdtitulo__icontains=cdtitulo,
                                tbprocessobase__nrprocesso__icontains=nrprocesso,
                                nrcpfrequerente__icontains=cpf,nmrequerente__icontains=requerente,
                                tbprocessobase__tbtitulo__tbstatustitulo__id__exact = 2)
    else:
        lista = Tbprocessorural.objects.all().filter(tbprocessobase__tbtitulo__tbstatustitulo__id__exact = 2)
    #lista = lista.order_by('tbprocessobase.tbtitulo')
    request.session[nome_relatorio] = lista
    return render_to_response('livro/consulta_nao_entregues.html' ,{'lista':lista}, context_instance = RequestContext(request))

    
@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):
    # montar objeto lista com os campos a mostrar no relatorio
    lista = request.session[nome_relatorio]
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, len(lista),  ods)
        
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Titulo' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Processo' ).setFontSize('14pt')
        sheet.getCell(2, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(3, 1).setAlignHorizontal('center').stringValue( 'CPF' ).setFontSize('14pt')
        sheet.getCell(4, 1).setAlignHorizontal('center').stringValue( 'Gleba' ).setFontSize('14pt')
        sheet.getCell(5, 1).setAlignHorizontal('center').stringValue( 'Municipio' ).setFontSize('14pt')
        sheet.getCell(6, 1).setAlignHorizontal('center').stringValue( 'Conjuge' ).setFontSize('14pt')
        sheet.getCell(7, 1).setAlignHorizontal('center').stringValue( 'CPF conjuge' ).setFontSize('14pt')
        sheet.getCell(8, 1).setAlignHorizontal('center').stringValue( 'Endereco' ).setFontSize('14pt')
        sheet.getCell(9, 1).setAlignHorizontal('center').stringValue( 'Contato' ).setFontSize('14pt')
        
        sheet.getRow(1).setHeight('14pt')
        #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbtitulo.cdtitulo)
            sheet.getCell(1, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nrprocesso)
            sheet.getCell(2, x+3).setAlignHorizontal('left').stringValue(obj.nmrequerente)
            sheet.getCell(3, x+3).setAlignHorizontal('left').stringValue(obj.nrcpfrequerente)
            sheet.getCell(4, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbgleba.nmgleba)
            sheet.getCell(5, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.tbmunicipio.nome_mun)
            sheet.getCell(6, x+3).setAlignHorizontal('left').stringValue(obj.nmconjuge)
            sheet.getCell(7, x+3).setAlignHorizontal('left').stringValue(obj.nrcpfconjuge)
            sheet.getCell(8, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nmendereco)
            sheet.getCell(9, x+3).setAlignHorizontal('left').stringValue(obj.tbprocessobase.nmcontato)
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

def validarProcesso(request_form):
    global fgexiste 
    base = request_form.POST['tbprocessobase'].replace('.','').replace('/','').replace('-','')
    processo = Tbprocessobase.objects.all().filter(nrprocesso = base)
    warning = True
    #verificar se processo existe e pertence a divisao do usuario
    if not processo:
        messages.add_message(request_form, messages.WARNING, 'O processo nao existe.')
        warning = False
   
    #verificar se o proceso  pertence a outra divisao
    if processo:
        processo = Tbprocessobase.objects.get(nrprocesso = base)
        divisao = Tbdivisao.objects.get(pk = Tbprocessobase.objects.get(nrprocesso = base).tbdivisao.id)
        if processo.tbdivisao.id != divisao.id:
            messages.add_message(request_form, messages.WARNING, 'O processo existe, mas pertence a outra divisao.')
            warning = False        
    
        #verifica se o processo base eh classificado como processo pai
        if processo.tbclassificacaoprocesso.id != 1:
            messages.add_message(request_form, messages.WARNING, 'Nao permitido associar titulo a  processo classificado como anexo/apenso.')
            warning = False        
        
        try:
            Tbtitulo.objects.get(tbprocessobase = processo.id) #this raises an ObjectDoesNotExist exception if it doesn't find a user with that username
        except ObjectDoesNotExist:
            warning = True  
        
        if Tbtitulo.objects.all().filter( tbprocessobase = processo.id):
            messages.add_message(request_form, messages.WARNING, 'Processo '+base+' ja esta associado a titulo ')
            warning = False
    
    return warning
