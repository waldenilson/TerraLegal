# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import json

data_atual = str(time.strftime("%d/%m/%Y"))

date_initial = '2013-11-25 08:00'

sql_processos ="""SELECT count(*) from tbprocessobase where tbclassificacaoprocesso_id = 1;"""
sql_pecas ="""SELECT count(*) from tbpecastecnicas;"""
sql_mov ="""SELECT count(*) from tbmovimentacao;"""
sql_tipo_processo = """ select t.nome, count(*)
                from tbprocessobase as b, tbtipoprocesso as t
                where b.tbtipoprocesso_id = t.id and
                tbclassificacaoprocesso_id = 1
                group by b.tbtipoprocesso_id, t.nome
                having count(*) > 0
                """
                
sql_titulo = """select s.sttitulo, count(*)
from  tbtitulo as t , tbstatustitulo as s
where t.tbstatustitulo_id = s.id
group by s.sttitulo
having count(*) > 0"""
                
                
sql_pend = """ select count(*) from tbpendencia where tbstatuspendencia_id = 2"""

sql_pend_chart = """ 
                select tipo.dspendencia , count(*) from tbpendencia pend, tbtipopendencia as tipo
                where pend.tbstatuspendencia_id = 2
                and pend.tbtipopendencia_id = tipo.id

                group by tbtipopendencia_id, tipo.dspendencia
                order by 1
                """

sql_mov_dia = """ select date_trunc('day',dtmovimentacao) , 
            count(*) from tbmovimentacao where dtmovimentacao > '%(date_mthago)s'
            group by date_trunc('day',dtmovimentacao) 
            order by date_trunc('day',dtmovimentacao);
            """


sql_processo_rural = """ select 'Processos', count(*)
                from tbprocessobase as b where b.tbtipoprocesso_id = 1 and
                tbclassificacaoprocesso_id = 1 """ 

sql_processo_com_peca = """ select 'Processo com peca', count(*) from tbprocessorural r 
        where r.nrcpfrequerente in (select nrcpfrequerente from tbpecastecnicas) and
        r.tbprocessobase_id in (select  id from tbprocessobase 
        where tbclassificacaoprocesso_id = 1 and tbtipoprocesso_id = 1)  """
sql_processo_sem_peca = """ select 'Processo sem peca', count(*) from tbprocessorural r left outer join  tbpecastecnicas p on r.nrcpfrequerente = p.nrcpfrequerente where p.nrcpfrequerente is null and r.tbprocessobase_id in (select  id from tbprocessobase where tbclassificacaoprocesso_id = 1 and tbtipoprocesso_id = 1)  """
sql_peca_com_processo = """ """
sql_peca_sem_processo = """ """

sql_cadastro =  """
                select dtcadastrosistema::timestamp::date , count(*)
                from tbprocessobase 
                where dtcadastrosistema > '20110101'
                group by dtcadastrosistema::timestamp::date
                having count(*) > 0
                order by 1
                """

qtd_usuarios = User.objects.count()

def milisec_datetime(d):
    return time.mktime(d.timetuple())*1000

def estatisticas(request):

    date_mthago = datetime.today()-timedelta(days=90) # date_wkago.strftime('%Y-%m-%d')
    
    cursor = connection.cursor()
    cursor.execute(sql_processos)
    qtd_processos = cursor.fetchone()
    qtd_processos = qtd_processos[0]
    
    cursor.execute(sql_pecas)
    qtd_pecas = cursor.fetchone()
    qtd_pecas = qtd_pecas[0]
    
    cursor.execute(sql_mov)
    qtd_mov = cursor.fetchone()
    qtd_mov = qtd_mov[0]
    
    
    cursor.execute(sql_pend)
    qtd_pend = cursor.fetchone()
    qtd_pend = qtd_pend[0]
    
    cursor.execute(sql_mov_dia % {'date_mthago':date_mthago})
    data = cursor.fetchall()
    data = [{"value":v, "label":milisec_datetime(k)} for k, v in data]
    tramitados_por_dia = json.dumps(data, cls=DjangoJSONEncoder)
    
    cursor.execute(sql_tipo_processo)
    qtd_tipos_proc = cursor.fetchall()
    qtd_tipos = [{"label": k, "value": v} for k, v in qtd_tipos_proc]
    qtd_tipos = json.dumps(qtd_tipos, cls=DjangoJSONEncoder)
    
    cursor.execute(sql_titulo)
    qtd_titulos = cursor.fetchall()
    qtd_titulo_registro = [{"label": k, "value": v} for k, v in qtd_titulos]
    qtd_titulo_registro = json.dumps(qtd_titulo_registro, cls=DjangoJSONEncoder)
    
    cursor.execute(sql_pend_chart)
    qtd_pend_chart = cursor.fetchall()
    qtd_pend_c = [{"label": k, "value": v} for k, v in qtd_pend_chart]
    qtd_pend_c = json.dumps(qtd_pend_c, cls=DjangoJSONEncoder)
    
    cursor.execute(sql_cadastro)
    qtd_cad = cursor.fetchall()
    qtd_cadastro = [{"label": milisec_datetime(k),"value": v} for k, v in qtd_cad]
    qtd_cadastro = json.dumps(qtd_cadastro, cls=DjangoJSONEncoder)
    
    cursor.execute(sql_processo_com_peca)
    qtd_verifica_1 = cursor.fetchone()
    teste = int(qtd_verifica_1[1])
    
    cursor.execute(sql_processo_sem_peca)
    qtd_verifica_2 = cursor.fetchone()
    teste2 = int(qtd_verifica_2[1])
    
    cursor.execute(sql_processo_rural)
    qtd_verifica_3 = cursor.fetchone()
    teste3 = int(qtd_verifica_3[1])
    
    qtd_bat = [ 
               {"label" : qtd_verifica_3[0] ,"value" : teste3},
               {"label" : qtd_verifica_1[0] ,"value" : teste}, 
               {"label" : qtd_verifica_2[0] ,"value" : -teste2} 
              ]
    return render(request, "web/estatisticas.html", {'qtd_processos': qtd_processos,'qtd_pecas':qtd_pecas,
                                                     'qtd_mov':qtd_mov,'qtd_tipos':qtd_tipos,'qtd_pend':qtd_pend,
                                                     'tramitados_por_dia': tramitados_por_dia,'qtd_bat':qtd_bat,
                                                     'qtd_pend_c':qtd_pend_c,'qtd_cadastro':qtd_cadastro,
                                                     'qtd_titulo_registro':qtd_titulo_registro
                                                     })

