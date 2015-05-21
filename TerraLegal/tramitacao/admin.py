
# -*- coding: UTF-8 -*-

from django.contrib import admin
from TerraLegal.tramitacao.models import Tbtipocaixa, Tbtipoprocesso, Tbstatuspendencia,\
    Tbpecastecnicas, Tbprocessobase,Tbclassificacaoprocesso, Tbsubarea, Tbcaixa,\
    Tbgleba, Tbcontrato, Tbsituacaoprocesso, Tbtipopendencia, AuthUser,\
    AuthUserGroups, AuthGroupPermissions, Tbmovimentacao, Tbprocessosanexos
from TerraLegal.calculo.models import TbtrMensal
from django.http.response import HttpResponse
import csv
import sqlite3
from datetime import datetime
from TerraLegal.tramitacao.models import Tbpendencia,Tbprocessorural, Tbprocessoclausula, Tbprocessourbano
from django.core import serializers

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
    elif inteiro == 3: mes_texto = "Marco"
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

def diferenca_mes(d2, d1):
    delta = 1
    print str(d1.month) + '/' + str(d1.year) 
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            print str(d1.month) + '/' + str(d1.year)
            delta += 1
        else:
            break
    return delta


def reader(csv_):
    with open(csv_, 'rb') as csvfile:
        aux = []
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            aux.append(row)

        lines = []
        x = 0
        for l in aux:
            if l:
                x += 1
            lines.append(l)

        print str(x)
        print len(lines)

def import_tr(csv_):
    trs = []
    aux = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            aux.append(row)

    lines = []
    for l in aux:
        #lines.append(l[0])
        sp = l[0].split('|')
        
#        print "ano "+sp[0] + ", mes "+str(1)+", valor "+sp[1]
        if sp[12] == '-':
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = None )
        else:    
            obj = TbtrMensal( ano = sp[0], mes = 12, valor = sp[12].replace(',','.') )
        obj.save()

                #obj = TbtrMensal(
                #        ano = sp[0],
                #        mes = x,
                #        valor = s
                #    )
                #obj.save()
        


    print len(lines)
    print lines


def batimento_processo(csv_):
    procs = []
    with open(csv_, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            procs.append(row)

    procs_line = []
    for proc in procs:
        if proc:
            #if not cpf[0] in cpfs_line:
            procs_line.append(proc[0])
        else:
            procs_line.append('0')

    processos = []
    for p in procs_line:
        obj = Tbprocessobase.objects.filter( nrprocesso = p.replace('/','').replace('.','').replace('-','') )
        if obj:
            print obj[0].nrprocesso+'|'+obj[0].tbcaixa.nmlocalarquivo
            processos.append( obj[0].tbcaixa.nmlocalarquivo.encode("utf-8") )
        else:
            processos.append( "-" )

    print len(procs_line)


    with open('/opt/tcu-localizacao.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in processos:
            writer.writerow({'caixa': str(cx) })


def buscar_processos_sem_pecas_sicop_sigef(request,csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)

    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            #if not cpf[0] in cpfs_line:
            cpfs_line.append(cpf[0])
        else:
            cpfs_line.append('0')
#    print len(cpfs_line)
    cont = 0
    procs = []

    rurais = Tbprocessorural.objects.filter( tbprocessobase__tbclassificacaoprocesso__id = 1, tbprocessobase__tbdivisao__id = AuthUser.objects.get( pk = request.user.id ).tbdivisao.id )
    p_rural_sem_peca = []
            
    for r in rurais:
        if not Tbpecastecnicas.objects.filter( nrcpfrequerente = r.nrcpfrequerente.replace('.','').replace('-','') ):
            p_rural_sem_peca.append( r )

    print 'Processos sem peca no sicop: '+str(len(p_rural_sem_peca))


    for r in p_rural_sem_peca:
        caixa = ''
        nome = ''
        cpf = ''
        if not r.nrcpfrequerente in cpfs_line and r.nrcpfrequerente != '99999999999' and r.nrcpfrequerente != '00000000000':
            caixa = r.tbprocessobase.tbcaixa.nmlocalarquivo
            nome = r.nmrequerente
            cpf = r.nrcpfrequerente
            print r.nmrequerente + '|' + r.nrcpfrequerente + '|' + r.tbprocessobase.tbcaixa.nmlocalarquivo + '|' + r.tbprocessobase.tbmunicipio.nome_mun + '|' + r.tbprocessobase.tbgleba.nmgleba
            procs.append( str(r.nmrequerente.encode("utf-8") + '|' + r.nrcpfrequerente.encode("utf-8") + '|' + r.tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8") +'|'+ r.tbprocessobase.tbmunicipio.nome_mun.encode("utf-8") +'|'+ r.tbprocessobase.tbgleba.nmgleba.encode("utf-8")) )
 
    print 'Processos sem peca no sicop nem no sigef: '+str(len(procs))

    print 'Processos sem peca no sicop mais que ja tem no sigef: '+str(len(p_rural_sem_peca)-len(procs))

    print len(cpfs_line)


    with open('/opt/export-sem-peca-sicop-sigef.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in procs:
            writer.writerow({'caixa': str(cx) })

def buscar_processos_cpfs_abril_sigef(csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)

    procs = []
    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            #if not cpf[0] in cpfs_line:
            cpfs_line.append(cpf[0])
        else:
            cpfs_line.append('0')
#    print len(cpfs_line)
    cont = 0
    for c in cpfs_line:
        res = Tbprocessorural.objects.filter( nrcpfrequerente = c, tbprocessobase__tbclassificacaoprocesso__id = 1 )
        caixa = ''
        nome = ''
        if res:
            cont += 1
            obj = res[0]
            caixa = obj.tbprocessobase.tbcaixa.nmlocalarquivo
            nome = obj.nmrequerente
#            print obj.tbprocessobase.nrprocesso + '|' + obj.nmrequerente + '|' + obj.nrcpfrequerente + '|' + obj.tbprocessobase.tbgleba.nmgleba + '|' + obj.tbprocessobase.tbcaixa.nmlocalarquivo
#            procs.append(obj)
        else:
            nome = 'none'
            caixa = '-'
        procs.append( caixa )
        print nome+'|'+caixa

    print len(cpfs_line)
    print len(procs)
    print str(cont)

    with open('/opt/export-sigef-titulacao.csv', 'w') as csvfile:
        fieldnames = ['caixa']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cx in procs:
            writer.writerow({'caixa': str(cx.encode("utf-8"))})


def buscar_processos_cpfs_sigef(csv_sigef):
    cpfs = []
    with open(csv_sigef, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            cpfs.append(row)


    procs = []
    cpfs_line = []
    for cpf in cpfs:
        if cpf:
            if not cpf[0] in cpfs_line:
                cpfs_line.append(cpf[0])
    print len(cpfs_line)

    for c in cpfs_line:
        res = Tbprocessorural.objects.filter( nrcpfrequerente = c, tbprocessobase__tbclassificacaoprocesso__id = 1 )
        if res:
            obj = res[0]
            print obj.tbprocessobase.nrprocesso + '|' + obj.nmrequerente + '|' + obj.nrcpfrequerente + '|' + obj.tbprocessobase.tbgleba.nmgleba + '|' + obj.tbprocessobase.tbcaixa.nmlocalarquivo
            procs.append(obj)

    print len(cpfs_line)
    print len(procs)


def list_json():
    pecas = ""
    peca = Tbpecastecnicas.objects.filter(nrcpfrequerente = 47551810625)
    for p in peca:
        if p.nrarea:
            pecas += str(p.nrarea)
        else:
            pecas += str('')
            
        pecas += '|'+str(p.tbmunicipio.nome_mun.encode("utf-8"))    
        pecas += '|'+str(p.tbgleba.nmgleba.encode("utf-8"))
        pecas += '|'+str(p.tbcontrato.nrcontrato.encode("utf-8"))
        if p.dsobservacao:
            pecas += '|'+str(p.dsobservacao.encode("utf-8"))
        else:
            pecas += '|'+str('')    
        pecas += 'FIMREG'

    print pecas


def buscar_pecas(cpf):
    pecas = ""
    peca = Tbpecastecnicas.objects.filter(nrcpfrequerente = cpf)
    if peca:
        for p in peca:
            if p.nrarea:
                pecas += str(p.nrarea)
            else:
                pecas += str('')
            if p.tbmunicipio:    
                pecas += '|'+str(p.tbmunicipio.nome_mun.encode("utf-8"))    
            else:
                pecas += '|'+str('')    
            if p.tbgleba:
                pecas += '|'+str(p.tbgleba.nmgleba.encode("utf-8"))
            else:
                pecas += '|'+str('')
            if p.tbcontrato:
                pecas += '|'+str(p.tbcontrato.nrcontrato.encode("utf-8"))
            else:
                pecas += '|'+str('')
            if p.dsobservacao:
                pecas += '|'+str(p.dsobservacao.encode("utf-8"))
            else:
                pecas += '|'+str('')    
            pecas += 'FIMREG'    
        return str(pecas)
    else:
        return ''


def buscar_anexos(id_processo):
    anexos = ""
    anexo = Tbprocessosanexos.objects.filter(tbprocessobase__id = id_processo)
    if anexo:
        for a in anexo:
            anexos += '|'+str(a.tbprocessobase_id_anexo.nrprocesso.encode("utf-8"))
            anexos += '|'+str(a.tbprocessobase_id_anexo.tbtipoprocesso.nome.encode("utf-8"))    
            if a.tbprocessobase_id_anexo.tbtipoprocesso.id == 1:
                req = Tbprocessorural.objects.filter( tbprocessobase__id = a.tbprocessobase_id_anexo.id )
                if req:
                    anexos += '|'+str(req[0].nmrequerente.encode("utf-8"))
                else:
                    anexos += '|'+str('')
            elif a.tbprocessobase_id_anexo.tbtipoprocesso.id == 2:
                req = Tbprocessoclausula.objects.filter( tbprocessobase__id = a.tbprocessobase_id_anexo.id )
                if req:
                    anexos += '|'+str(req[0].nmrequerente.encode("utf-8"))
                else:
                    anexos += '|'+str('')
            else:
                req = Tbprocessourbano.objects.filter( tbprocessobase__id = a.tbprocessobase_id_anexo.id )
                if req:
                    anexos += '|'+str(req[0].nmpovoado.encode("utf-8"))
                else:
                    anexos += '|'+str('')

            anexos += '|'+str(a.auth_user.username.encode("utf-8"))
            anexos += '|'+str(a.dtanexado.day)+'/'+str(a.dtanexado.month)+'/'+str(a.dtanexado.year)

            anexos += 'FIMREG'
        return str(anexos)
    else:
        return ''

def buscar_movimentacoes(id_processo):
    movimentacoes = ""
    mov = Tbmovimentacao.objects.filter(tbprocessobase__id = id_processo)
    if mov:
        for m in mov:
            movimentacoes += '|'+str(m.tbcaixa.nmlocalarquivo.encode("utf-8"))
            movimentacoes += '|'+str(m.tbcaixa_id_origem.nmlocalarquivo.encode("utf-8"))    
            movimentacoes += '|'+str(m.auth_user.username.encode("utf-8"))
            movimentacoes += '|'+str(m.dtmovimentacao.day)+'/'+str(m.dtmovimentacao.month)+'/'+str(m.dtmovimentacao.year)
            movimentacoes += 'FIMREG'
        return str(movimentacoes)
    else:
        return ''
    


def buscar_pendencias(id_processo):
    pendencias = ""
    pend = Tbpendencia.objects.filter(tbprocessobase__id = id_processo)
    if pend:
        for p in pend:
            pendencias += '|'+str(p.dsdescricao.encode("utf-8"))
            if p.dsparecer:
                pendencias += '|'+str(p.dsparecer.encode("utf-8"))
            else:
                pendencias += '|'+str('')    
            pendencias += '|'+str(p.tbtipopendencia.dspendencia.encode("utf-8"))
            pendencias += '|'+str(p.tbstatuspendencia.dspendencia.encode("utf-8"))
            pendencias += '|'+str(p.auth_user_updated.username.encode("utf-8"))
            pendencias += '|'+str(p.dtpendencia.day)+'/'+str(p.dtpendencia.month)+'/'+str(p.dtpendencia.year)
            pendencias += 'FIMREG'
        return str(pendencias)
    else:
        return ''
    

def export_to_sqlite_android(arquivo):
    conn = sqlite3.connect(arquivo)
    cursor = conn.cursor()
#    c.execute("create table processo (id integer primary key,numero TEXT, cadastro_pessoa TEXT")

    data1 = datetime.now()

    #select id,nrcpfrequerente,nmrequerente,tbcaixa_id,dsobservacao,nrarea,tbgleba_id,tbcontrato_id,nrentrega,tbmunicipio_id from tbpecastecnicas

    #PROCESSOS RURAIS
    rurais = Tbprocessorural.objects.all().order_by("tbprocessobase__id")
    for r in rurais:
        identificador = str(r.tbprocessobase.id)
        numero = str(r.tbprocessobase.nrprocesso)
        cadastro_pessoa = str(r.nrcpfrequerente.encode("utf-8"))
        nome = str(r.nmrequerente.encode("utf-8").replace('\'',''))

        if r.nmconjuge:
            subnome = str(r.nmconjuge.encode("utf-8").replace('\'',''))
        else:
            subnome = str(r.nmconjuge)    

        localizacao = str(r.tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8").replace('\'',''))
        gleba = str(r.tbprocessobase.tbgleba.nmgleba.encode("utf-8").replace('\'',''))
        tipo = str(r.tbprocessobase.tbtipoprocesso.nome.encode("utf-8"))
        classificacao = str(r.tbprocessobase.tbclassificacaoprocesso.nmclassificacao.encode("utf-8"))
        
        if r.tbprocessobase.tbmunicipio.nome_mun:
            municipio_declarado = str(r.tbprocessobase.tbmunicipio.nome_mun.encode("utf-8").replace('\'',''))
        else:
            municipio_declarado = str(r.tbprocessobase.tbmunicipio.nome_mun)

        if r.tbprocessobase.nmendereco:
            endereco = str(r.tbprocessobase.nmendereco.encode("utf-8").replace('\'',''))
        else:
            endereco = str(r.tbprocessobase.nmendereco)
        if r.tbprocessobase.nmcontato:    
            contato = str(r.tbprocessobase.nmcontato.encode("utf-8").replace('\'',''))
        else:
            contato = str(r.tbprocessobase.nmcontato)

        pendencias = buscar_pendencias(r.tbprocessobase.id)

        movimentacoes = buscar_movimentacoes(r.tbprocessobase.id)

        pecas = buscar_pecas(r.tbprocessobase.id)

        anexos = buscar_anexos(r.tbprocessobase.id)

        sql = "insert into processo ('id','numero','cadastro_pessoa','nome','subnome','localizacao','gleba','tipo','classificacao','municipio_declarado','endereco','contato','pendencias','movimentacoes','pecas','anexos') values ("+identificador+",'"+numero+"','"+cadastro_pessoa+"','"+nome+"','"+subnome+"','"+localizacao+"','"+gleba+"','"+tipo+"','"+classificacao+"','"+municipio_declarado+"','"+endereco+"','"+contato+"','"+pendencias+"','"+movimentacoes+"','"+pecas+"','"+anexos+"')"
        print sql
        cursor.execute(sql)

    #PROCESSOS P80
    clausulas = Tbprocessoclausula.objects.all().order_by("tbprocessobase__id")
    for c in clausulas:
        identificador = str(c.tbprocessobase.id)
        numero = str(c.tbprocessobase.nrprocesso)
        cadastro_pessoa = str(c.nrcpfrequerente.encode("utf-8"))
        nome = str(c.nmrequerente.encode("utf-8").replace('\'',''))

        if c.nminteressado:
            subnome = str(c.nminteressado.encode("utf-8").replace('\'',''))
        else:
            subnome = str(c.nminteressado)    

        localizacao = str(c.tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8").replace('\'',''))
        gleba = str(c.tbprocessobase.tbgleba.nmgleba.encode("utf-8").replace('\'',''))
        tipo = str(c.tbprocessobase.tbtipoprocesso.nome.encode("utf-8"))
        classificacao = str(c.tbprocessobase.tbclassificacaoprocesso.nmclassificacao.encode("utf-8"))
        
        if c.tbprocessobase.tbmunicipio.nome_mun:
            municipio_declarado = str(c.tbprocessobase.tbmunicipio.nome_mun.encode("utf-8").replace('\'',''))
        else:
            municipio_declarado = str(c.tbprocessobase.tbmunicipio.nome_mun)

        if c.tbprocessobase.nmendereco:
            endereco = str(c.tbprocessobase.nmendereco.encode("utf-8").replace('\'',''))
        else:
            endereco = str(c.tbprocessobase.nmendereco)
        if c.tbprocessobase.nmcontato:    
            contato = str(c.tbprocessobase.nmcontato.encode("utf-8").replace('\'',''))
        else:
            contato = str(c.tbprocessobase.nmcontato)

        pendencias = buscar_pendencias(c.tbprocessobase.id)

        movimentacoes = buscar_movimentacoes(c.tbprocessobase.id)

        pecas = buscar_pecas(c.tbprocessobase.id)

        anexos = buscar_anexos(c.tbprocessobase.id)
        
        sql = "insert into processo ('id','numero','cadastro_pessoa','nome','subnome','localizacao','gleba','tipo','classificacao','municipio_declarado','endereco','contato','pendencias','movimentacoes','pecas','anexos') values ("+identificador+",'"+numero+"','"+cadastro_pessoa+"','"+nome+"','"+subnome+"','"+localizacao+"','"+gleba+"','"+tipo+"','"+classificacao+"','"+municipio_declarado+"','"+endereco+"','"+contato+"','"+pendencias+"','"+movimentacoes+"','"+pecas+"','"+anexos+"')"
        print sql
        cursor.execute(sql)

    #PROCESSOS URBANOS
    urbanos = Tbprocessourbano.objects.all().order_by("tbprocessobase__id")
    for u in urbanos:
        identificador = str(u.tbprocessobase.id)
        numero = str(u.tbprocessobase.nrprocesso)
        cadastro_pessoa = str(u.nrcnpj.encode("utf-8"))
        nome = str(u.nmpovoado.encode("utf-8").replace('\'',''))

        if u.dsprojetoassentamento:
            subnome = str(u.dsprojetoassentamento.encode("utf-8").replace('\'',''))
        else:
            subnome = str(u.dsprojetoassentamento)    

        localizacao = str(u.tbprocessobase.tbcaixa.nmlocalarquivo.encode("utf-8").replace('\'',''))
        gleba = str(u.tbprocessobase.tbgleba.nmgleba.encode("utf-8").replace('\'',''))
        tipo = str(u.tbprocessobase.tbtipoprocesso.nome.encode("utf-8"))
        classificacao = str(u.tbprocessobase.tbclassificacaoprocesso.nmclassificacao.encode("utf-8"))
        
        if u.tbprocessobase.tbmunicipio.nome_mun:
            municipio_declarado = str(u.tbprocessobase.tbmunicipio.nome_mun.encode("utf-8").replace('\'',''))
        else:
            municipio_declarado = str(u.tbprocessobase.tbmunicipio.nome_mun)

        if u.tbprocessobase.nmendereco:
            endereco = str(u.tbprocessobase.nmendereco.encode("utf-8").replace('\'',''))
        else:
            endereco = str(u.tbprocessobase.nmendereco)
        if u.tbprocessobase.nmcontato:    
            contato = str(u.tbprocessobase.nmcontato.encode("utf-8").replace('\'',''))
        else:
            contato = str(u.tbprocessobase.nmcontato)

        pendencias = buscar_pendencias(u.tbprocessobase.id)

        movimentacoes = buscar_movimentacoes(u.tbprocessobase.id)

        pecas = buscar_pecas(u.tbprocessobase.id)

        anexos = buscar_anexos(u.tbprocessobase.id)
        
        sql = "insert into processo ('id','numero','cadastro_pessoa','nome','subnome','localizacao','gleba','tipo','classificacao','municipio_declarado','endereco','contato','pendencias','movimentacoes','pecas','anexos') values ("+identificador+",'"+numero+"','"+cadastro_pessoa+"','"+nome+"','"+subnome+"','"+localizacao+"','"+gleba+"','"+tipo+"','"+classificacao+"','"+municipio_declarado+"','"+endereco+"','"+contato+"','"+pendencias+"','"+movimentacoes+"','"+pecas+"','"+anexos+"')"
        print sql
        cursor.execute(sql)

    data2 = datetime.now()

    print str(data2 - data1)

    conn.commit()
    conn.close()



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

