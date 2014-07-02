'''
Created on 01/07/2014

@author: eduardo
'''

from __future__ import unicode_literals
from django.db import models

class Tbsituacao(models.Model):
    cdTabela = models.CharField(max_length=30)
    dsSituacao = models.CharField(max_length=50)
    class Meta:
        db_table = 'tbsituacao'
    


class Tbservidor(models.Model):
    nmservidor = models.CharField(max_length=100)
    nmunidade = models.CharField(max_length=100)
    nmlotacao = models.CharField(max_length=30)
    cdsiape = models.CharField(max_length=7)
    nrcpf = models.CharField(max_length=11)
    dsportariacargo = models.TextField()
    dsportaria = models.TextField()
    nmcargo = models.CharField(max_length=80)
    nrtelefone1 = models.CharField(max_length=10)
    nrtelefone2 = models.CharField(max_length=10)
    email = models.CharField(max_length=75)
    dsatividades = models.TextField()
    tbdivisao = models.ForeignKey('sicop.Tbdivisao')
    id = models.AutoField(primary_key=True)
    nmcontrato = models.CharField(max_length=20)
    dtnascimento = models.DateField()
    
    class Meta:
        db_table = 'tbservidor'

class Tbferias(models.Model):
    tbservidor = models.ForeignKey('Tbservidor')
    nrAno = models.IntegerField()
    dtInicio1 = models.DateField()
    nrDias1 = models.IntegerField()
    stSituacao1 = models.ForeignKey('Tbsituacao',related_name='situacao_p1')
    dtInicio2 = models.DateTimeField(null=True,blank=True)
    nrDias2 = models.IntegerField(null=True,blank=True)
    stSituacao2 = models.ForeignKey('Tbsituacao',related_name='situacao_p2')
    dtInicio3 = models.DateField(null=True,blank=True)
    nrDias3 = models.IntegerField(null=True,blank=True)
    stSituacao3 = models.ForeignKey('Tbsituacao',related_name='situacao_p3')
    stAntecipa = models.NullBooleanField()
    stDecimoTerceiro = models.NullBooleanField()
    dsObservacao = models.TextField(blank=True)
    class Meta:
        db_table = 'tbferias'

