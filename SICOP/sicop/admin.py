from django.contrib import admin
from sicop.models import Tbtipocaixa, Tbtipoprocesso, Tbstatuspendencia,\
    Tbpecastecnicas, Tbclassificacaoprocesso, Tbsubarea, Tbcaixa,\
    Tbgleba, Tbcontrato, Tbsituacaoprocesso, Tbtipopendencia, AuthUser,\
    AuthUserGroups
import xlwt
from django.http.response import HttpResponse

def verificar_permissao_grupo(usuario, grupos):
    if usuario:
        permissao = False
        obj_usuarios = AuthUserGroups.objects.all().filter( user = usuario.id )
        for obj in obj_usuarios:
            for obj_g in grupos:
                if obj.user.id == usuario.id and obj.group.name == str(obj_g):
                    permissao = True
        return permissao
    return False

def relatorio_base_excel(nome, header, lista):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('my_sheet')  
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    # write the header
    for hcol, hcol_data in enumerate(header): # [(0,'Header 1'), (1, 'Header 2'), (2,'Header 3'), (3,'Header 4')]
           sheet.write(0, hcol, hcol_data, style=xlwt.Style.default_style)
    # write your data, you can also get it from your model    
    data = []
    for obj in lista:
        data2 = [obj.nmlocalarquivo, obj.tbtipocaixa.nmtipocaixa]
        data.append(data2)
    
    for row, row_data in enumerate(data, start=1): # start from row no.1
           for col, col_data in enumerate(row_data):
                 sheet.write(row, col, col_data, style=xlwt.Style.default_style)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+str(nome)+'.xls'
    book.save(response)
    return response


# tbtipocaixa,
# tbcaixa,
# tbmunicipio, 
# tbtipopendencia,
# tbstatuspendencia, 
# tbsubarea, 
# tbconjuge,
# tbcontrato,
# tbgleba,
# tbsituacaoprocessourbano,
# tbclassificacaoprocesso,
# tbtipoprocesso

# TABELAS BASICAS (VARIAVEIS STATUS E/OU TIPOS)
#admin.site.register(Tbtipoprocesso)
#admin.site.register(Tbtipopendencia)
#admin.site.register(Tbsituacaoprocesso)
#admin.site.register(Tbclassificacaoprocesso)
#admin.site.register(Tbstatuspendencia)
#admin.site.register(Tbpecastecnicas)

# TABELAS CONTROLE CRUD (MIGRACAO)
# admin.site.register(Tbmunicipio)
#admin.site.register(Tbsubarea)
#admin.site.register(Tbcontrato)
#admin.site.register(Tbgleba)
#admin.site.register(Tbcaixa)
#admin.site.register(Tbtipocaixa)
admin.site.register(AuthUser)

