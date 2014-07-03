'''
Created on 03/07/2014

@author: eduardo
'''

from __future__ import unicode_literals
from django.db import models

class Tbtipotitulo(models.Model):
    cdtipo = models.CharField(max_length=10, blank=True)
    dstipo = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtipotitulo'
        
class Tbstatustitulo(models.Model):
    id = models.AutoField(primary_key=True)
    sttitulo = models.CharField(max_length=30)
    class Meta:
        db_table = 'tbstatustitulo'
        
class Tbtitulo(models.Model):
    cdtitulo = models.CharField(max_length=8)
    #tbprocessobase = models.ForeignKey(Tbprocessobase,blank=True)
    tbstatustitulo = models.ForeignKey(Tbstatustitulo,blank=True)
    tbtipotitulo = models.ForeignKey(Tbtipotitulo,blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtitulo'
