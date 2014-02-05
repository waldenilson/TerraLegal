from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from sicop.models import Tbtipoprocesso, Tbcaixa, Tbgleba, Tbmunicipio, AuthUser,\
    AuthGroup, Tbprocessobase, Tbprocessorural, Tbclassificacaoprocesso, Tbsituacaoprocesso,\
    Tbpecastecnicas, Tbmovimentacao, Tbtipodocumento, Tbdocumentobase,\
    Tbdocumentomemorando, Tbservidor, Tbdocumentoservidor
from sicop.forms import FormProcessoRural, FormProcessoBase
from django.contrib import messages
from django.http.response import HttpResponseRedirect, HttpResponse
import datetime
from reportlab.platypus.flowables import Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import time
from reportlab.platypus.doctemplate import SimpleDocTemplate

@permission_required('servidor.documento_memorando_consulta', login_url='/excecoes/permissao_negada/', raise_exception=True)
def consulta(request):
    return render_to_response('sicop/restrito/documento/memorando/consulta.html',{}, context_instance = RequestContext(request))    
    
@permission_required('servidor.documento_memorando_cadastro', login_url='/excecoes/permissao_negada/', raise_exception=True)
def cadastro(request):
    tipodocumento = Tbtipodocumento.objects.all()
    div_documento = "memorando"
    escolha = "tbdocumentomemorando"
    
    if request.method == "POST":
        if validacao(request, "cadastro"):
                        
            servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
            docservidor = Tbdocumentoservidor.objects.filter( tbdocumentobase__id = id )
                
            result = {}
            for obj in servidor:
                achou = False
                for obj2 in docservidor:
                    if obj.id == obj2.tbservidor.id:
                        result.setdefault(obj.nmservidor,True)
                        achou = True
                        break
                if not achou:
                    result.setdefault(obj.nmservidor, False)
            result = sorted(result.items())
           
                        
                        
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

@permission_required('servidor.documento_memorando_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def criacao(request, id):   
    
    memorando = get_object_or_404(Tbdocumentomemorando, id=id)
    base  = get_object_or_404(Tbdocumentobase, id=memorando.tbdocumentobase.id)
    print base.nmdocumento
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+base.nmdocumento+'.pdf"'

    doc = SimpleDocTemplate(response, rightMargin=72,leftMargin=72, topMargin=72,bottomMargin=18)
    
    Story=[]
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
     
    formatted_time = time.ctime()
    full_name = memorando.nmassunto
     
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    ptext = '<font size=12>%s</font>' % formatted_time
     
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
     
    # Create return address
    ptext = '<font size=12>%s</font>' % full_name
    Story.append(Paragraph(ptext, styles["Normal"]))       
     
    Story.append(Spacer(1, 12))
    Story.append(Spacer(1, 12))
       
     
#    ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
#            You will receive %s issues at the excellent introductory price of $%s. Please respond by\
#            %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
#                                                                                                   issueNum,
#                                                                                                    subPrice,
#                                                                                                    limitedDate,
#                                                                                                    freeGift)
    
    corpo = memorando.nmmensagem
    
    ptext = '<font size=12>'+corpo+'</font>'
    
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))
          
    ptext = '<font size=12>'+memorando.nmlocal+'</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=12>'+memorando.nmremetente+'</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=12>'+memorando.nmdestinatario+'</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    
    doc.build(Story)
    
    return response

@permission_required('servidor.documento_memorando_edicao', login_url='/excecoes/permissao_negada/', raise_exception=True)
def edicao(request, id):
        
    memorando = get_object_or_404(Tbdocumentomemorando, id=id)
    base  = get_object_or_404(Tbdocumentobase, id=memorando.tbdocumentobase.id)
     
    if validacao(request, "edicao"):

        servidor = Tbservidor.objects.filter( tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
        
        # verificando os grupos do usuario
        for obj in servidor:
            print 'AQUI'
            if request.POST.get(obj.nmservidor, False):
                #verificar se esse grupo ja esta ligado ao usuario
                res = Tbdocumentoservidor.objects.filter( tbdocumentobase__id = id, tbservidor__id = obj.id )
                if not res:
                    # inserir ao authusergroups
                    ug = Tbdocumentoservidor( tbdocumentobase = Tbdocumentobase.objects.get( pk = id ),
                                          tbservidor = Tbservidor.objects.get( pk = obj.id ) )
                    ug.save()
                    #print obj.name + ' nao esta ligado a este usuario'
            else:
                #verificar se esse grupo foi desligado do usuario
                res = Tbdocumentoservidor.objects.filter( tbdocumentobase__id = id, tbservidor__id = obj.id )
                if res:
                    # excluir do authusergroups
                    for aug in res:
                        aug.delete()
                    #print obj.name + ' desmarcou deste usuario'

        
        
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
                                       id = memorando.id,
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

