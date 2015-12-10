from django.db import models
from TerraLegal.tramitacao.models import AuthUser, Tbprocessobase

class Memorando(models.Model):
    id = models.AutoField(primary_key=True)
    auth_user = models.ForeignKey(AuthUser)
    data_cadastro = models.DateTimeField(null=False)
    data_modificacao = models.DateTimeField(auto_now=True)
    numero = models.IntegerField(null=False)
    data_documento = models.DateField(null=False)
    assunto = models.CharField(max_length=80)
    mensagem = models.TextField(blank=True)
    remetente = models.CharField(max_length=80)
    destinatario = models.CharField(max_length=80)
    localidade = models.CharField(max_length=80)
    signatario = models.CharField(max_length=80)
    cargo_signatario = models.CharField(max_length=80)
    class Meta:
        db_table = '"documento"."memorando"'    

class Sobreposicao(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    auth_user = models.ForeignKey(AuthUser)
    data_cadastro = models.DateTimeField(null=True, blank=True)
    data_modificacao = models.DateTimeField(auto_now=True)
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
    forma_georreferenciamento = models.CharField(max_length=80, blank=True)
    data_atualizacao = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = '"documento"."sobreposicao"'

class DespachoAprovacaoRegional(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    auth_user = models.ForeignKey(AuthUser)
    data_cadastro = models.DateTimeField(null=True, blank=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    numero = models.IntegerField(blank=True)
    ano = models.IntegerField(blank=True)
    assunto = models.CharField(max_length=120)
    cidade = models.CharField(max_length=80)
    folha = models.IntegerField(blank=True)
    data_despacho = models.DateField(null=True, blank=True)
    class Meta:
        db_table = '"documento"."despacho_aprovacao_regional"'