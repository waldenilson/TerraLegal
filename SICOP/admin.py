
# -*- coding: UTF-8 -*-

from django.contrib import admin
from sicop.models import Tbtipocaixa, Tbtipoprocesso, Tbstatuspendencia,\
    Tbpecastecnicas, Tbclassificacaoprocesso, Tbsubarea, Tbcaixa,\
    Tbgleba, Tbcontrato, Tbsituacaoprocesso, Tbtipopendencia, AuthUser,\
    AuthUserGroups, AuthGroupPermissions
from django.http.response import HttpResponse

def verificar_permissao_grupo(usuario, grupos):
    if usuario:
        permissao = False
        obj_usuarios = AuthUserGroups.objects.filter( user = usuario.id )
        for obj in obj_usuarios:
            for obj_g in grupos:
                if obj.user.id == usuario.id and obj.group.name == str(obj_g):
                    permissao = True
        return permissao
    return False

def verificar_permissoes(grupo, permissoes):
    if grupo:
        permissao = False
        obj_grupos = AuthGroupPermissions.objects.filter( group = grupo.id )
        for obj in obj_grupos:
            for obj_g in permissoes:
                if obj.group.id == grupo.id and obj.permission.id == obj_g.id:
                    permissao = True
        return permissao
    return False


def mes_do_ano_texto(inteiro):
    mes_texto = ""
    
    if inteiro == 1: mes_texto = "Janeiro"
    elif inteiro == 2: mes_texto = "Fevereiro"
    elif inteiro == 3: mes_texto = "Março"
    elif inteiro == 4: mes_texto = "Abril"
    elif inteiro == 5: mes_texto = "Maio"
    elif inteiro == 6: mes_texto = "Junho"
    elif inteiro == 7: mes_texto = "Julho"
    elif inteiro == 8: mes_texto = "Agosto"
    elif inteiro == 9: mes_texto = "Setembro"
    elif inteiro == 10: mes_texto = "Outubro"
    elif inteiro == 11: mes_texto = "Novembro"
    elif inteiro == 12: mes_texto = "Dezembro"
    
    return mes_texto

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

