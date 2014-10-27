# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Tbcalculotitulo(models.Model):
    tbextrato = models.ForeignKey('Tbextrato',blank=True)
    parcela = models.IntegerField()
    cdrecolhimento = models.CharField(blank=True,max_length=20)
    nrreferencia = models.CharField(blank=True,max_length=20)
    dtvencimento = models.DateField()
    cdug = models.CharField(blank=True,max_length=20)
    vlprincipal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vldesconto = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vldeducoes = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlcorrecao = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlmulta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vljuros = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vlacrescimos = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vltotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_user = models.ForeignKey('tramitacao.AuthUser')
    stpaga  = models.BooleanField(default=False)
    stgerada  = models.BooleanField(default=False)
    dtentrega = models.DateField(null=True)
    dtrequerimento = models.DateField(null=True)
    dtgeracao = models.DateField(null=True)
    dtpagamento = models.DateField(null=True)

    
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcalculotitulo'



class Tbextrato(models.Model):
    id_req = models.TextField(blank=True)
    cpf_req = models.TextField(blank=True)
    origem = models.TextField(blank=True)
    dap = models.TextField(blank=True)
    nome_req = models.TextField(blank=True)
    apelido_req = models.TextField(blank=True)
    cooperativa_req = models.TextField(blank=True)
    nome_mae_req = models.TextField(blank=True)
    doc_id_req = models.TextField(blank=True)
    tipo_doc_id_req = models.TextField(blank=True)
    orgao_emiss_doc_id_req = models.TextField(blank=True)
    data_nasc_req = models.DateField(null=True, blank=True)
    nacionalidade_req = models.TextField(blank=True)
    naturalidade_req = models.TextField(blank=True)
    sexo_req = models.TextField(blank=True)
    estado_civil_req = models.TextField(blank=True)
    endereco_req = models.TextField(blank=True)
    telefone_req = models.TextField(blank=True)
    cpf_conj = models.TextField(blank=True)
    nome_conj = models.TextField(blank=True)
    nome_mae_conj = models.TextField(blank=True)
    doc_id_conj = models.TextField(blank=True)
    tipo_doc_id_conj = models.TextField(blank=True)
    orgao_emiss_doc_id_conj = models.TextField(blank=True)
    data_nasc_conj = models.DateField(null=True, blank=True)
    nacionalidade_conj = models.TextField(blank=True)
    estado_civil_conj = models.TextField(blank=True)
    sexo_conj = models.TextField(blank=True)
    naturalidade_conj = models.TextField(blank=True)
    numero_processo = models.TextField(blank=True)
    sncr = models.TextField(blank=True)
    nome_imovel = models.TextField(blank=True)
    atividade_economica = models.TextField(blank=True)
    data_ocupacao_originaria = models.DateField(null=True, blank=True)
    data_ocupacao_atual = models.DateField(null=True, blank=True)
    ocupante_primitivo = models.TextField(blank=True)
    posse_mansa_pacifica = models.TextField(blank=True)
    doc_expedido_orgao_publico = models.TextField(blank=True)
    indicacao_acesso = models.TextField(blank=True)
    distancia_nucleo_urbano = models.TextField(blank=True)
    tipo_acesso = models.TextField(blank=True)
    nome_gleba = models.TextField(blank=True)
    nome_gleba_cadastro = models.TextField(blank=True)
    area = models.TextField(blank=True)
    area_medida = models.TextField(blank=True)
    tamanho_modulos_fiscais = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    area_total_imovel = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    area_maior_fracao_minima = models.TextField(blank=True)
    uf_imovel = models.TextField(blank=True)
    cod_municipio = models.TextField(blank=True)
    nome_municipio = models.TextField(blank=True)
    situacao_processo = models.TextField(blank=True)
    data_inicio_situacao_atual = models.DateField(null=True, blank=True)
    entidade_cadastramento = models.TextField(blank=True)
    responsavel_cadastramento = models.TextField(blank=True)
    inspetor_cadastramento = models.TextField(blank=True)
    data_cadastro = models.DateField(null=True, blank=True)
    inspetor_transmissao = models.TextField(blank=True)
    data_transmissao = models.DateField(null=True, blank=True)
    numero_assentimento = models.CharField(max_length=50, blank=True)
    ano_assentimento = models.DecimalField(null=True, max_digits=4, decimal_places=0, blank=True)
    valor_imovel = models.DecimalField(null=True, max_digits=65535, decimal_places=65535, blank=True)
    data_vencimento_primeira_prestacao = models.DateField(null=True, blank=True)
    data_inicio_etapa_anterior = models.DateField(null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = 'tbextrato'

