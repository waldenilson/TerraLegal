from django.db import models
from TerraLegal.tramitacao.models import Tbdivisao, AuthUser, Tbservidor, Tbprocessobase

class DocumentoBase(models.Model):
    titulo = models.CharField(max_length=80, blank=True)
    data_cadastro = models.DateTimeField(null=True, blank=True)
    data_movimentacao = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    tbdivisao = models.ForeignKey(Tbdivisao)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = '"documento"."documento_base"'
        
class DocumentoServidor(models.Model):
    documento = models.ForeignKey(DocumentoBase)
    servidor = models.ForeignKey(Tbservidor)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = '"documento"."documento_servidor"'

class DocumentoSobreposicao(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.ForeignKey(DocumentoBase)
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    forma_georreferenciamento = models.CharField(max_length=80, blank=True)
    data_atualizacao = models.DateTimeField(null=True, blank=True)
    bl_item_1 = models.BooleanField()
    txt_item_1 = models.TextField(blank=True)
    bl_item_2 = models.BooleanField()
    txt_item_2 = models.TextField(blank=True)
    bl_item_3 = models.BooleanField()
    txt_item_3 = models.TextField(blank=True)
    bl_item_4 = models.BooleanField()
    txt_item_4 = models.TextField(blank=True)
    bl_item_5 = models.BooleanField()
    txt_item_5 = models.TextField(blank=True)
    bl_item_6 = models.BooleanField()
    txt_item_6 = models.TextField(blank=True)
    bl_item_7 = models.BooleanField()
    txt_item_7 = models.TextField(blank=True)
    bl_item_8 = models.BooleanField()
    txt_item_8 = models.TextField(blank=True)
    bl_item_9 = models.BooleanField()
    txt_item_9 = models.TextField(blank=True)
    bl_item_10 = models.BooleanField()
    txt_item_10 = models.TextField(blank=True)
    bl_item_11 = models.BooleanField()
    txt_item_11 = models.TextField(blank=True)
    class Meta:
        db_table = '"documento"."documento_sobreposicao"'
