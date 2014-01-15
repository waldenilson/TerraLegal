from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbtipodocumento, Tbdocumentobase,\
    Tbdocumentomemorando
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect
import datetime

#10.12.0.60

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/documento/memorando/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.all()
    
    div_documento = "memorando"
    escolha = "tbdocumentomemorando"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):
            
            # cadastrando o registro processo base            
            f_base = Tbdocumentobase (
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentomemorando' ),
                                    linkdocumento = 'arquivo.pdf',
                                    dtdocumento = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()
            
            f_memorando = Tbdocumentomemorando (
                                       nmassunto = request.POST['nmassunto'],
                                       nmlocal = request.POST['nmlocal'],
                                       nmremetente = request.POST['nmremetente'],
                                       nmdestinatario = request.POST['nmdestinatario'],
                                       nmmensagem = request.POST['nmmensagem'],
                                       tbdocumentobase = f_base,
                                       )
            f_memorando.save()
            
            return HttpResponseRedirect("/sicop/restrito/documento/consulta/")
        
    return render_to_response('sicop/restrito/documento/cadastro.html',
        {'tipodocumento':tipodocumento, 'documento':escolha, 'div_documento':div_documento}, context_instance = RequestContext(request))    

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def link_arquivo(request, id):    
    return HttpResponseRedirect("/sicop/restrito/documento/arquivo.pdf")

@permission_required('sicop.caixa_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
    
    memorando = get_object_or_404(Tbdocumentomemorando, id=id)
    base  = get_object_or_404(Tbprocessobase, id=memorando.tbdocumentobase.id)
      
    if validacao(request, "edicao"):
         # cadastrando o registro processo base            
            f_base = Tbdocumentobase (
                                    id = base.id,
                                    nmdocumento = request.POST['nmdocumento'],
                                    tbtipodocumento = Tbtipodocumento.objects.get( tabela = 'tbdocumentomemorando' ),
                                    linkdocumento = 'arquivo.pdf',
                                    dtdocumento = datetime.datetime.now(),
                                    auth_user = AuthUser.objects.get( pk = request.user.id ),
                                    tbdivisao = AuthUser.objects.get( pk = request.user.id ).tbdivisao
                                    )
            f_base.save()

            f_memorando = Tbdocumentomemorando (
                                       nmassunto = request.POST['nmassunto'],
                                       nmlocal = request.POST['nmlocal'],
                                       nmremetente = request.POST['nmremetente'],
                                       nmdestinatario = request.POST['nmdestinatario'],
                                       nmmensagem = request.POST['nmmensagem'],
                                       tbdocumentobase = f_base,
                                       )
            f_memorando.save()
            
            return HttpResponseRedirect("/sicop/restrito/documento/edicao/"+str(base.id)+"/")
    
    return render_to_response('sicop/restrito/documento/memorando/edicao.html',
                              {'base':base,'memorando':memorando},
                               context_instance = RequestContext(request))   

def validacao(request_form, metodo):
    warning = True
    if request_form.POST['nmdocumento'] == '':
        messages.add_message(request_form,messages.WARNING,'Informe o nome do documento')
        warning = False
    
    return warning 

