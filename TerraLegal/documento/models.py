from django.db import models
from sicop.models import Tbdivisao, AuthUser, Tbservidor

class Tbtipodocumento(models.Model):
    nmtipodocumento = models.CharField(max_length=80, blank=True)
    desctipodocumento = models.TextField(blank=True)
    tabela = models.CharField(max_length=50, blank=True)
    coridentificacao = models.CharField(max_length=20, blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtipodocumento'

class Tbdocumentobase(models.Model):
    nmdocumento = models.CharField(max_length=80, blank=True)
    tbtipodocumento = models.ForeignKey('Tbtipodocumento')
    dtcadastrodocumento = models.DateTimeField(null=True, blank=True)
    dtdocumento = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    tbdivisao = models.ForeignKey(Tbdivisao)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbdocumentobase'

        
class Tbdocumentoservidor(models.Model):
    tbdocumentobase = models.ForeignKey(Tbdocumentobase)
    tbservidor = models.ForeignKey(Tbservidor)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbdocumentoservidor'

class Tbdocumentomemorando(models.Model):
    tbdocumentobase = models.ForeignKey(Tbdocumentobase)
    nrsisdoc = models.CharField(max_length=20, blank=True)
    nrsufixosisdoc = models.CharField(max_length=20, blank=True)
    nmassunto = models.CharField(max_length=100, blank=True)
    nmlocal = models.CharField(max_length=100, blank=True)
    nmremetente = models.CharField(max_length=100, blank=True)
    nmdestinatario = models.CharField(max_length=100, blank=True)
    nmmensagem = models.TextField(blank=True)
    blcircular = models.BooleanField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbdocumentomemorando'
  
class Tbdocumentooficio(models.Model):
    tbdocumentobase = models.ForeignKey(Tbdocumentobase)
    nrsisdoc = models.CharField(max_length=20, blank=True)
    nrsufixosisdoc = models.CharField(max_length=20, blank=True)
    nmtratamento = models.CharField(max_length=80, blank=True)
    nmcargo = models.CharField(max_length=80, blank=True)
    nmempresa = models.CharField(max_length=80, blank=True)
    nmassunto = models.CharField(max_length=100, blank=True)
    nmlocal = models.CharField(max_length=100, blank=True)
    nmdestinatario = models.CharField(max_length=100, blank=True)
    nrcep = models.CharField(max_length=10, blank=True)
    nmendereco = models.TextField(blank=True)
    nmcidade = models.CharField(max_length=100, blank=True)
    nrtelefone = models.CharField(max_length=20, blank=True)
    nmemail = models.TextField(blank=True)
    nmmensagem = models.TextField(blank=True)
    blcircular = models.BooleanField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbdocumentooficio'

class Tbdocumentovr(models.Model):
    id = models.AutoField(primary_key=True)
    tbdocumentobase = models.ForeignKey(Tbdocumentobase, null=True, blank=True)
    dtinicioservicos = models.DateTimeField(null=True, blank=True)
    objetivo = models.TextField(blank=True)
    destino = models.CharField(max_length=120, blank=True)
    tempodias = models.IntegerField(null=True, blank=True)
    motorista = models.CharField(max_length=120, blank=True)
    usuarios = models.TextField(blank=True)
    localviatura = models.CharField(max_length=80, blank=True)
    dtsolicitante = models.DateField(null=True, blank=True)
    dtautorizado = models.DateField(null=True, blank=True)
    veiculo = models.CharField(max_length=80, blank=True)
    placa = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'tbdocumentovr'

class Tbdocumentorme(models.Model):
    id = models.AutoField(primary_key=True)
    tbdocumentobase = models.ForeignKey(Tbdocumentobase, null=True, blank=True)
    dtperiodo = models.DateField(null=True, blank=True)
    nrordem = models.IntegerField(null=True, blank=True)
    solicitante = models.CharField(max_length=120, blank=True)
    class Meta:
        db_table = 'tbdocumentorme'

class Tbdocumentomaterialrme(models.Model):
    id = models.AutoField(primary_key=True)
    especificacao = models.CharField(max_length=120, blank=True)
    unidade = models.CharField(max_length=80, blank=True)
    qtdsolicitada = models.IntegerField(null=True, blank=True)
    tbdocumentorme = models.ForeignKey('Tbdocumentorme', null=True, blank=True)
    class Meta:
        db_table = 'tbdocumentomaterialrme'
        
class Tbdocumentotru(models.Model):
    id = models.AutoField(primary_key=True)
    tbdocumentobase_id = models.IntegerField(null=True, blank=True)
    nmlocalidade = models.CharField(max_length=80, blank=True)
    nome = models.CharField(max_length=80, blank=True)
    nrsiape = models.CharField(max_length=20, blank=True)
    nrcpf = models.CharField(max_length=11, blank=True)
    endereco = models.TextField(blank=True)
    justificativa = models.TextField(blank=True)
    dtiniciocedencia = models.DateField(null=True, blank=True)
    dtfimcedencia = models.DateField(null=True, blank=True)
    declaracao = models.TextField(blank=True)
    class Meta:
        db_table = 'tbdocumentotru'

class Tbdocumentobmp(models.Model):
    id = models.AutoField(primary_key=True)
    tbdocumentobase_id = models.IntegerField(null=True, blank=True)
    coddestino = models.CharField(max_length=20, blank=True)
    localdestino = models.CharField(max_length=120, blank=True)
    observacao = models.TextField(blank=True)
    dtrecebimento = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'tbdocumentobmp'
