# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.contrib.gis.db import models
#from django.db import models

class Indigena(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    geom = models.PolygonField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = 'indigena'


class TbparcelaGeo(models.Model):
    gid = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=254, blank=True)
    gleba = models.CharField(max_length=254, blank=True)
    nome_deten = models.CharField(max_length=254, blank=True)
    cpf_detent = models.CharField(max_length=254, blank=True)
    natureza = models.CharField(max_length=254, blank=True)
    situacao_p = models.CharField(max_length=254, blank=True)
    regional = models.CharField(max_length=254, blank=True)
    uf_id = models.IntegerField()
    id = models.IntegerField()
    nr_process = models.CharField(max_length=24, blank=True)
    planilha_o = models.CharField(max_length=154, blank=True)
    data_recep = models.DateField(blank=True)
#    data_situacao_processo = models.DateField(blank=True)
    protocolo = models.CharField(max_length=28, blank=True)
    status = models.CharField(max_length=254, blank=True)
    identifica = models.CharField(max_length=54, blank=True)
    contrato = models.CharField(max_length=54, blank=True)
    id_contrat = models.IntegerField()
    empresa = models.CharField(max_length=254, blank=True)
    fiscal = models.CharField(max_length=254, blank=True)
    email = models.CharField(max_length=254, blank=True)
    fronteira = models.CharField(max_length=254, blank=True)
    area_ha_ut = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    migrada = models.CharField(max_length=254, blank=True)
    municipio = models.CharField(max_length=120)
    gleba_situ = models.CharField(max_length=254, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()
    class Meta:
        db_table = 'tbparcela_geo'
'''
class Tbparcela(models.Model):
    dsjson = models.TextField(blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbparcela'

class TbparcelaGeo(models.Model):
    area_total = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    kml = models.TextField(blank=True)
    id_sigef = models.CharField(max_length=80, blank=True)
    nome = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=80, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbparcela_geo'

class TbCPFParcelaGeo(models.Model):
    tbparcela_geo = models.ForeignKey(TbparcelaGeo, null=False)
    cpf = models.CharField(max_length=11, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcpf_parcela_geo'

class TbCNPJParcelaGeo(models.Model):
    tbparcela_geo = models.ForeignKey(TbparcelaGeo, null=False)
    cnpj = models.CharField(max_length=20, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcnpj_parcela_geo'

class TbMunicipioParcelaGeo(models.Model):
    tbparcela_geo = models.ForeignKey(TbparcelaGeo, null=False)
    ibge = models.CharField(max_length=20, blank=True)
    nome = models.CharField(max_length=120, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    area = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    area_perc = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbmunicipio_parcela_geo'
'''
