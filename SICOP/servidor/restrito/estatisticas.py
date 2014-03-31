# -*- coding: utf-8 -*-

from django.core.serializers.json import DjangoJSONEncoder

from django.db import connection

from django.contrib.auth.models import User

from django.shortcuts import render

from datetime import datetime, timedelta
import time
import json


date_initial = '2013-11-25 08:00'

sql_processos ="""SELECT count(*) from tbprocessobase"""

qtd_usuarios = User.objects.count()
def milisec_datetime(d):
    return time.mktime(d.timetuple())*1000
def estatistica(request):

    date_wkago = datetime.today()-timedelta(days=7) # date_wkago.strftime('%Y-%m-%d')
    #print date_wkago
    
    cursor = connection.cursor()
    cursor.execute(sql_processos)
    qtd_processos = cursor.fetchall()
    
    return render(request, "web/estatisticas.html", {'qtd_processos': qtd_processos,})
