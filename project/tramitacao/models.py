# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

#from django.contrib.gis.db import models
from django.db import models
from project.servidor.models import Tbservidor

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    tbdivisao = models.ForeignKey('Tbdivisao')
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    tbdivisao = models.ForeignKey('Tbdivisao')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'django_site'

class Tbcaixa(models.Model):
    nmlocalarquivo = models.CharField(max_length=80, blank=True)
    tbtipocaixa = models.ForeignKey('Tbtipocaixa')
    id = models.AutoField(primary_key=True)
    tbdivisao = models.ForeignKey('Tbdivisao', null=True, blank=True)
    blativo = models.BooleanField()
    class Meta:
        db_table = 'tbcaixa'
    def __unicode__(self):
        return self.nmlocalarquivo

class Tbclassificacaoprocesso(models.Model):
    nmclassificacao = models.CharField(max_length=80, blank=True)
    tbdivisao = models.ForeignKey('Tbdivisao', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbclassificacaoprocesso'

class Tbcontrato(models.Model):
    nrcontrato = models.CharField(max_length=10, blank=False, null=False)
    nmempresa = models.CharField(max_length=100, blank=False, null=False)
    tbdivisao = models.ForeignKey('Tbdivisao', null=True, blank=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbcontrato'

class Tbdivisao(models.Model):
    nmdivisao = models.CharField(max_length=80, blank=True)
    dsdivisao = models.TextField(blank=True)
    tbuf = models.ForeignKey('Tbuf', null=True, blank=True)
    id = models.AutoField(primary_key=True)
    nrclasse = models.SmallIntegerField()
    class Meta:
        db_table = 'tbdivisao'
    def __str__(self):
        return self.nmdivisao


class Tbgleba(models.Model):
    #cdgleba = models.IntegerField(null=True, blank=True)
    nmgleba = models.CharField(max_length=80, blank=False,null=False)
    tbsubarea = models.ForeignKey('Tbsubarea')
    tbuf = models.ForeignKey('Tbuf', null=False, blank=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbgleba'        
    def __str__(self):
        return self.nmgleba

class Tbmovimentacao(models.Model):
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    dtmovimentacao = models.DateTimeField(null=True, blank=True)
    tbcaixa_id_origem = models.ForeignKey(Tbcaixa, db_column='tbcaixa_id_origem', related_name='tbcaixa_id_origem')
    tbcaixa = models.ForeignKey(Tbcaixa)
    auth_user = models.ForeignKey(AuthUser)
    nrdias = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbmovimentacao'

class Tbmunicipio(models.Model):
    nome_mun_maiusculo = models.CharField(max_length=50, db_column='Nome_Mun_Maiusculo', blank=True) # Field name made lowercase.
    nome_mun = models.CharField(max_length=50, db_column='Nome_Mun', blank=True) # Field name made lowercase.
    codigo_mun = models.IntegerField(null=True, db_column='Codigo_Mun', blank=True) # Field name made lowercase.
    regiao = models.CharField(null=True, max_length=50, db_column='Regiao', blank=True) # Field name made lowercase.
    uf = models.CharField(max_length=2, db_column='UF', blank=True) # Field name made lowercase.
    sr = models.CharField(null=True, max_length=50, db_column='SR', blank=True) # Field name made lowercase.
    codigo_uf = models.ForeignKey('Tbuf', null=True, db_column='Codigo_UF', blank=True) # Field name made lowercase.
    populacao = models.CharField(null=True, max_length=50, db_column='Populacao', blank=True) # Field name made lowercase.
    nrmodulofiscal = models.IntegerField(null=True, blank=True)
    nrfracaominima = models.IntegerField(null=True, blank=True)
    id = models.AutoField(primary_key=True)
    vlterranua = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = 'tbmunicipio'

class Tbpecastecnicas(models.Model):
    cdpeca = models.CharField(max_length=50, blank=True)
    tbcontrato = models.ForeignKey(Tbcontrato)
    nrentrega = models.CharField(max_length=10, blank=True)
    nrcpfrequerente = models.CharField(max_length=14, blank=True)
    nmrequerente = models.CharField(max_length=80, blank=True)
    stenviadobrasilia = models.BooleanField()
    stpecatecnica = models.BooleanField()
    stanexadoprocesso = models.BooleanField()
    dsobservacao = models.TextField(blank=True)
    tbcaixa = models.ForeignKey(Tbcaixa)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    tbgleba = models.ForeignKey(Tbgleba)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    tbmunicipio = models.ForeignKey(Tbmunicipio, null=True)
    stassentamento = models.BooleanField()
    class Meta:
        db_table = 'tbpecastecnicas'

class Tbpendencia(models.Model):
    nrcodigo = models.CharField(max_length=50, blank=True)
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    tbtipopendencia = models.ForeignKey('Tbtipopendencia')
    dsdescricao = models.TextField(blank=True)
    dtpendencia = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    tbstatuspendencia = models.ForeignKey('Tbstatuspendencia')
    dsparecer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    auth_user_updated = models.ForeignKey(AuthUser, related_name="auth_user_updated")
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbpendencia'

class Tbpregao(models.Model):
    nrpregao = models.CharField(max_length=30, blank=False,null=True)
    dspregao = models.TextField(blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=False, blank=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbpregao'

class Tbsituacao(models.Model):
    cdTabela = models.CharField(max_length=30)
    dsSituacao = models.CharField(max_length=50)
    class Meta:
        db_table = 'tbsituacao'


class Tbprocessobase(models.Model):
    nrprocesso = models.CharField(max_length=17, blank=True)
    tbgleba = models.ForeignKey(Tbgleba,null=True)
    tbcaixa = models.ForeignKey(Tbcaixa)
    tbmunicipio = models.ForeignKey(Tbmunicipio,null=True)
    auth_user = models.ForeignKey(AuthUser)
    tbtipoprocesso = models.ForeignKey('Tbtipoprocesso')
    tbetapaatual = models.ForeignKey('Tbetapa', null=True, blank=True)
    dtcadastrosistema = models.DateTimeField(null=True, blank=True)
    tbclassificacaoprocesso = models.ForeignKey(Tbclassificacaoprocesso, null=True, blank=True)
    tbdivisao = models.ForeignKey('Tbdivisao')
    nmendereco = models.TextField(blank=True)
    nmcontato = models.TextField(blank=True)
    tbtitulo = models.ForeignKey('livro.Tbtitulo',null=True)
    tbmunicipiodomicilio = models.ForeignKey(Tbmunicipio, related_name='tbmunicipiodomicilio_id', null=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbprocessobase'

class Tbprocessoclausula(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nminteressado = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    nrcpfinteressado = models.CharField(max_length=11, blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    dsobs = models.TextField(blank=True)
    stprocuracao = models.BooleanField( blank=True)
    dttitulacao = models.DateField(null=True, blank=True)
    dtrequerimento = models.DateField(null=True, blank=True)
    #dtnascimento = models.CharField(max_length=20, blank=True)
    dtnascimento = models.DateField(null=True, blank=True)
    nmtitulo = models.CharField(max_length=80, blank=True)
    tptitulo = models.CharField(max_length=80, blank=True)
    nmimovel = models.CharField(max_length=80, blank=True)
    nmloteimovel = models.CharField(max_length=80, blank=True)
    blgeoimovel = models.BooleanField()
    dsprioridade = models.CharField(max_length=40, blank=True)
    stcertquitacao = models.BooleanField( blank=True)
    stcertliberacao = models.BooleanField( blank=True)
    id = models.AutoField(primary_key=True)
       
    class Meta:
        db_table = 'tbprocessoclausula'

class Tbprocessorural(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    blconjuge = models.BooleanField( blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    nrcpfconjuge = models.CharField(max_length=11, blank=True)
    nmconjuge = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbprocessorural'

class Tbprocessosanexos(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    tbprocessobase_id_anexo = models.ForeignKey(Tbprocessobase, db_column='tbprocessobase_id_anexo', related_name='tbprocessobase_id_anexo')
    dtanexado = models.DateTimeField(null=True, blank=True)
    auth_user = models.ForeignKey(AuthUser)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbprocessosanexos'

class Tbprocessourbano(models.Model):
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    nmpovoado = models.CharField(max_length=80, blank=True)
    nrcnpj = models.CharField(max_length=14, blank=True)
    dtaberturaprocesso = models.DateTimeField(null=True, blank=True)
    dttitulacao = models.DateTimeField(null=True, blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    nrdomicilios = models.IntegerField(null=True, blank=True)
    nrhabitantes = models.IntegerField(null=True, blank=True)
    tbpregao = models.ForeignKey('Tbpregao')
    tbcontrato = models.ForeignKey('Tbcontrato')
    tbsituacaogeo = models.ForeignKey('Tbsituacaogeo', null=True, blank=True)
    dsprojetoassentamento = models.CharField(max_length=80, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbprocessourbano'

class Tbsituacaogeo(models.Model):
    nmsituacaogeo = models.CharField(max_length=80, blank=True)
    dssituacaogeo = models.TextField(blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbsituacaogeo'

class Tbsituacaoprocesso(models.Model):
    nmsituacao = models.CharField(max_length=80, blank=True)
    dssituacao = models.TextField(blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbsituacaoprocesso'

class Tbstatuspendencia(models.Model):
    stpendencia = models.IntegerField(null=True, blank=True)
    dspendencia = models.CharField(max_length=100, blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbstatuspendencia'
        
class Tbsubarea(models.Model):
    cdsubarea = models.CharField(max_length=10, blank=True)
    nmsubarea = models.CharField(max_length=80, blank=False,null=False)
    tbdivisao = models.ForeignKey(Tbdivisao, null=False, blank=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbsubarea'
    def __str__(self):
        return self.nmsubarea

class Tbtipocaixa(models.Model):
    nmtipocaixa = models.CharField(max_length=80, blank=False,null=False)
    desctipocaixa = models.TextField(blank=True)
    #tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True) removido 20140214 
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtipocaixa'

class Tbtipopendencia(models.Model):
    dspendencia = models.CharField(max_length=50, blank=True)
    tbtipoprocesso = models.ForeignKey('Tbtipoprocesso')
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtipopendencia'

class Tbtipoprocesso(models.Model):
    nome = models.CharField(max_length=80, blank=True)
    tabela = models.CharField(max_length=50, blank=True)
    coridentificacao = models.CharField(max_length=20, blank=True)
    tbdivisao = models.ForeignKey(Tbdivisao, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtipoprocesso'
        
class Tbuf(models.Model):
    sigla = models.CharField(max_length=2, blank=True)
    nmuf = models.CharField(max_length=50, blank=True)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbuf'
    def __str__(self):
        return self.sigla

'''
    Models FLuxo do processo
'''

class Tbetapa(models.Model):
    nmfase = models.CharField(max_length=80, blank=True)
    titulo = models.CharField(max_length=120, blank=True)
    tbtipoprocesso = models.ForeignKey(Tbtipoprocesso, null=True, blank=True)
    dsfase = models.TextField(blank=True)
    blativo = models.BooleanField()
    blinicial = models.BooleanField()
    ordem = models.IntegerField()
    tbdivisao = models.ForeignKey('Tbdivisao')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbetapa'

class Tbprocessobaseetapa(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase, null=True, blank=True)
    tbetapa = models.ForeignKey(Tbetapa, null=True, blank=True)
    dsparecer = models.TextField(blank=True)
    class Meta:
        db_table = 'tbprocessobaseetapa'

class Tbchecklist(models.Model):
    nmchecklist = models.TextField(blank=True)
    tbetapa = models.ForeignKey(Tbetapa, null=True, blank=True)
    dschecklist = models.TextField(blank=True)
    blcustomdate = models.BooleanField()
    blcustomtext = models.BooleanField()
    bl_data_prazo = models.BooleanField()
    lbcustomdate = models.CharField(max_length=80, blank=True)
    lbcustomtext = models.CharField(max_length=80, blank=True)
    nrprazo = models.IntegerField()
    blprogramacao = models.BooleanField( blank=True) 
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbchecklist'

class Tbchecklistprocessobase(models.Model):
    tbchecklist = models.ForeignKey(Tbchecklist, null=True, blank=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase, null=True, blank=True)
    blnao_obrigatorio = models.BooleanField()
    blsanado = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    dtcustom = models.DateTimeField(null=True, blank=True)
    nmcustom = models.CharField(max_length=80, blank=True)
    bl_em_programacao = models.BooleanField( blank=True) 
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbchecklistprocessobase'

class Tbtransicao(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase, null=True, blank=True)
    tbetapa = models.ForeignKey(Tbetapa, null=True, blank=True)
    dttransicao = models.DateTimeField( null=False )
    auth_user = models.ForeignKey(AuthUser)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbtransicao'

class Tbetapaanterior(models.Model):
    tbetapa = models.ForeignKey(Tbetapa, null=True, blank=True)
    tbanterior = models.ForeignKey(Tbetapa, db_column='tbanterior', related_name='tbanterior')
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbetapaanterior'

class Tbetapaposterior(models.Model):
    tbetapa = models.ForeignKey(Tbetapa, null=True, blank=True)
    tbposterior = models.ForeignKey(Tbetapa, db_column='tbposterior', related_name='tbposterior')
    blsequencia = models.BooleanField( null=False )
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbetapaposterior'

class Tbloganalise(models.Model):
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    auth_user = models.ForeignKey(AuthUser)
    tbetapa = models.ForeignKey(Tbetapa, null=True)
    tbcaixa = models.ForeignKey(Tbcaixa, null=True)
    dtanalise = models.DateTimeField(null=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'tbloganalise'
        
