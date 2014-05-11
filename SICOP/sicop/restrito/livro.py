from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtitulo, Tbstatustitulo, Tbtipotitulo, AuthUser, Tbprocessobase, Tbprocessorural,Tbdivisao, Tbpecastecnicas
from django.http import HttpResponseRedirect
from django.contrib import messages
from sicop.relatorio_base import relatorio_ods_base_header, relatorio_ods_base, relatorio_csv_base,\
    relatorio_pdf_base_header, relatorio_pdf_base,\
    relatorio_pdf_base_header_title
from django.http.response import HttpResponse
from odslib import ODS
import csv
from django.core.exceptions import ObjectDoesNotExist
from TerraLegal import settings

nome_relatorio      = "relatorio_livro"
response_consulta  = "/sicop/restrito/livro/consulta/"
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
        nrprocesso  = request.POST['nrprocesso']
        lista = Tbtitulo.objects.all().filter( cdtitulo__icontains=cdtitulo,tbprocessobase__nrprocesso__icontains=nrprocesso )
        lista = lista.order_by('cdtitulo')
        request.session[nome_relatorio] = lista
        return render_to_response('sicop/restrito/livro/consulta.html' ,{'lista':lista}, context_instance = RequestContext(request))
    return render_to_response('sicop/restrito/livro/consulta.html',context_instance = RequestContext(request))

@permission_required('sicop.caixa_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    if request.method == "POST":
        next = request.GET.get('next', '/')
        if validarProcesso(request):
            print 'status titulo ' + str(request.POST['tbstatustitulo'])
            processobase = Tbprocessobase.objects.get( nrprocesso = 
                    request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
            f_titulo = Tbtitulo(
                            cdtitulo = request.POST['cdtitulo'],
                            tbprocessobase = processobase,
                            tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                            tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo'])
                        )
            f_titulo.save()
            if next == "/":
                return HttpResponseRedirect(response_consulta)
            else:    
                return HttpResponseRedirect(next)
    return render_to_response('sicop/restrito/livro/cadastro.html',{"statustitulo":statustitulo,"tipotitulo":tipotitulo}, context_instance = RequestContext(request))

@permission_required('sicop.livro_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    statustitulo = Tbstatustitulo.objects.all()
    tipotitulo  = Tbtipotitulo.objects.all()
    
    if request.method == "POST":
        titulo = get_object_or_404(Tbtitulo, id=id)
        if not request.user.has_perm('sicop.livro_edicao'):
            return HttpResponseRedirect('/excecoes/permissao_negada/')
        processobase = Tbprocessobase.objects.get( nrprocesso = 
                    request.POST['tbprocessobase'].replace('.','').replace('/','').replace('-',''))
        if validacao(request):
            rural = Tbprocessorural.objects.get( tbprocessobase = processobase.id)
            peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente.replace('.','').replace('-','') )
            f_titulo = Tbtitulo(
                cdtitulo = request.POST['cdtitulo'],
                tbprocessobase = processobase,
                tbstatustitulo  = Tbstatustitulo.objects.get(id = request.POST['tbstatustitulo']),
                tbtipotitulo    = Tbtipotitulo.objects.get(id = request.POST['tbtipotitulo']),  
                id = titulo.id
                )
            f_titulo.save()
            return HttpResponseRedirect("/sicop/restrito/livro/edicao/"+str(id)+"/")
    else:
        titulo = get_object_or_404(Tbtitulo, id=id)
        divisao = titulo.tbprocessobase.tbdivisao.id
        processobase = get_object_or_404(Tbprocessobase, nrprocesso = titulo.tbprocessobase.nrprocesso)
        rural = Tbprocessorural.objects.get( tbprocessobase = processobase.id)
        peca = Tbpecastecnicas.objects.all().filter( nrcpfrequerente = rural.nrcpfrequerente)
        if divisao <> AuthUser.objects.get(pk = request.user.id).tbdivisao.id:
            return HttpResponseRedirect('/excecoes/permissao_negada/')
    
    return render_to_response('sicop/restrito/livro/edicao.html', {"titulo":titulo,"statustitulo":statustitulo,"tipotitulo":tipotitulo,"processobase":processobase,"peca":peca,"rural":rural}, context_instance = RequestContext(request))

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def relatorio_ods(request):
    # montar objeto lista com os campos a mostrar no relatorio/pdf
    lista = request.session[nome_relatorio]
    if lista:
        ods = ODS()
        sheet = relatorio_ods_base_header(planilha_relatorio, titulo_relatorio, ods)
        # subtitle
        sheet.getCell(0, 1).setAlignHorizontal('center').stringValue( 'Nome' ).setFontSize('14pt')
        sheet.getCell(1, 1).setAlignHorizontal('center').stringValue( 'Tipo' ).setFontSize('14pt')
        sheet.getRow(1).setHeight('20pt')
        #TRECHO PERSONALIZADO DE CADA CONSULTA
        #DADOS
        x = 0
        for obj in lista:
            sheet.getCell(0, x+2).setAlignHorizontal('center').stringValue(obj.nmlocalarquivo)
            sheet.getCell(1, x+2).setAlignHorizontal('center').stringValue(obj.tbtipocaixa.nmtipocaixa)    
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

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
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
