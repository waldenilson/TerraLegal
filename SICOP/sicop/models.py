#from django.db import models

# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.templatetags.l10n import localize

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    tbdivisao = models.ForeignKey('Tbdivisao')
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
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
#    id = models.IntegerField(primary_key=True)
    nmlocalarquivo = models.CharField(max_length=80, blank=True)
    qtdprocessos = models.IntegerField(null=True, blank=True)
    tbtipocaixa = models.ForeignKey('Tbtipocaixa')
    def __unicode__(self):
        return self.nmlocalarquivo
    class Meta:
        db_table = 'tbcaixa'

class Tbclassificacaoprocesso(models.Model):
#    id = models.IntegerField(primary_key=True)
    nmclassificacao = models.CharField(max_length=80, blank=True)
    def __unicode__(self):
        return self.nmclassificacao
    class Meta:
        db_table = 'tbclassificacaoprocesso'

class Tbcontrato(models.Model):
#    id = models.IntegerField(primary_key=True)
    nrcontrato = models.CharField(max_length=10, blank=True)
    nmempresa = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return self.nrcontrato

    class Meta:
        db_table = 'tbcontrato'
        
class Tbdivisao(models.Model):
    id = models.AutoField(primary_key=True)
    nmdivisao = models.CharField(max_length=80, blank=True)
    dsdivisao = models.TextField(blank=True)
    tbuf = models.ForeignKey('Tbuf', null=True, blank=True)
    class Meta:
        db_table = 'tbdivisao'

class Tbgleba(models.Model):
#    id = models.IntegerField(primary_key=True)
    cdgleba = models.IntegerField(null=True, blank=True)
    nmgleba = models.CharField(max_length=80, blank=True)
    tbsubarea = models.ForeignKey('Tbsubarea')
    def __unicode__(self):
        return self.nmgleba
    class Meta:
        db_table = 'tbgleba'

class Tbmovimentacao(models.Model):
    id = models.IntegerField(primary_key=True)
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    tbcaixa_id = models.ForeignKey(Tbcaixa, db_column='tbcaixa_id',related_name='tbcaixa_id')
    tbcaixa_id_origem = models.ForeignKey(Tbcaixa, db_column='tbcaixa_id_origem',related_name='tbcaixa_id_origem')
    auth_user = models.ForeignKey(AuthUser)
    dtmovimentacao = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'tbmovimentacao'

class Tbmunicipio(models.Model):
    id = models.AutoField(primary_key=True)
    nome_mun_maiusculo = models.CharField(max_length=50, db_column='Nome_Mun_Maiusculo', blank=True) # Field name made lowercase.
    nome_mun = models.CharField(max_length=50, db_column='Nome_Mun', blank=True) # Field name made lowercase.
    codigo_mun = models.IntegerField(null=True, db_column='Codigo_Mun', blank=True) # Field name made lowercase.
    regiao = models.CharField(max_length=50, db_column='Regiao', blank=True) # Field name made lowercase.
    nome_estado = models.CharField(max_length=50, db_column='Nome_Estado', blank=True) # Field name made lowercase.
    uf = models.CharField(max_length=2, db_column='UF', blank=True) # Field name made lowercase.
    sr = models.CharField(max_length=50, db_column='SR', blank=True) # Field name made lowercase.
    codigo_uf = models.ForeignKey('Tbuf', null=True, db_column='Codigo_UF', blank=True) # Field name made lowercase.
    populacao = models.CharField(max_length=50, db_column='Populacao', blank=True) # Field name made lowercase.
    def __unicode__(self):
        return self.nome_mun
    class Meta:
        db_table = 'tbmunicipio'

class Tbmunicipiomodulo(models.Model):
    id = models.AutoField(primary_key=True)
    tbmunicipio = models.ForeignKey(Tbmunicipio)
    nrcodigo = models.CharField(max_length=10, blank=True)
    nrmodulorural = models.IntegerField(null=True, blank=True)
    cdibge = models.CharField(max_length=7, blank=True)
    cdpostal = models.CharField(max_length=10, blank=True)
    nrmodulofiscal = models.IntegerField(null=True, blank=True)
    nrfracaominima = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'tbmunicipiomodulo'

class Tbpecastecnicas(models.Model):
    id = models.AutoField(primary_key=True)
    tbcaixa = models.ForeignKey(Tbcaixa)
    tbcontrato = models.ForeignKey(Tbcontrato)
    tbgleba = models.ForeignKey(Tbgleba)
    cdpeca = models.CharField(max_length=50, blank=True)
    nrentrega = models.CharField(max_length=10, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    nmrequerente = models.CharField(max_length=80, blank=True)
    stenviadobrasilia = models.BooleanField(null=False, blank=True)
    stpecatecnica = models.BooleanField(null=False, blank=True)
    stanexadoprocesso = models.BooleanField(null=False, blank=True)
    dsobservacao = models.TextField(blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    class Meta:
        db_table = 'tbpecastecnicas'

class Tbpendencia(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    auth_user = models.ForeignKey(AuthUser)
    tbtipopendencia = models.ForeignKey('Tbtipopendencia')
    tbstatuspendencia = models.ForeignKey('Tbstatuspendencia')
    dsdescricao = models.TextField(blank=True)
    dtpendencia = models.DateTimeField(null=True, blank=True)
    nrcodigo = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'tbpendencia'

class Tbprocessorural(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey('Tbprocessobase')
    tbclassificacaoprocesso = models.ForeignKey(Tbclassificacaoprocesso)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    nmconjuge = models.CharField(max_length=100, blank=True)
    nrcpfconjuge = models.CharField(max_length=11, blank=True)
    blconjuge = models.BooleanField(null=False, blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'tbprocessorural'

class Tbprocessobase(models.Model):
    id = models.AutoField(primary_key=True)
    nrprocesso = models.CharField(max_length=17, blank=True)
    tbtipoprocesso = models.ForeignKey('Tbtipoprocesso')
    tbsituacaoprocesso = models.ForeignKey('Tbsituacaoprocesso')
    auth_user = models.ForeignKey(AuthUser)
    tbmunicipio = models.ForeignKey('Tbmunicipio')
    dtcadastrosistema = models.DateTimeField(null=True, blank=True)
    tbcaixa = models.ForeignKey('Tbcaixa')
    tbgleba = models.ForeignKey('Tbgleba')
    class Meta:
        db_table = 'tbprocessobase'

class Tbprocessoclausula(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    tbclassificacaoprocesso = models.ForeignKey(Tbclassificacaoprocesso)
    nmrequerente = models.CharField(max_length=100, blank=True)
    nminteressado = models.CharField(max_length=100, blank=True)
    nrcpfrequerente = models.CharField(max_length=11, blank=True)
    nrcpfinteressado = models.CharField(max_length=11, blank=True)
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    dttitulacao = models.DateTimeField(null=True, blank=True)
    cdstatus = models.IntegerField(null=True, blank=True)
    dsobs = models.TextField(blank=True)
    stprocuracao = models.BooleanField(null=False, blank=True)
    class Meta:
        db_table = 'tbprocessoclausula'

class Tbprocessosanexos(models.Model):
    id = models.AutoField(primary_key=True)
    tbcaixa = models.ForeignKey(Tbcaixa)
    tbprocessobase = models.ForeignKey(Tbprocessobase,db_column='tbprocessobase_id',related_name='tbprocessobase_id')
    tbprocessobase_id_anexo = models.ForeignKey(Tbprocessobase, db_column='tbprocessobase_id_anexo',related_name='tbprocessobase_id_anexo')
    auth_user = models.ForeignKey(AuthUser)
    dtanexado = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'tbprocessosanexos'

class Tbprocessourbano(models.Model):
    id = models.AutoField(primary_key=True)
    tbprocessobase = models.ForeignKey(Tbprocessobase)
    tbcontrato = models.ForeignKey(Tbcontrato)
    nmpovoado = models.CharField(max_length=80, blank=True)
    nrcnpj = models.CharField(max_length=14, blank=True)
    dtaberturaprocesso = models.DateTimeField(null=True, blank=True)
    dttitulacao = models.DateTimeField(null=True, blank=True)
    tbsituacaogeo = models.ForeignKey('Tbsituacaogeo')
    nrarea = models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True)
    nrperimetro = models.DecimalField(null=True, max_digits=18, decimal_places=4, blank=True)
    nrdomicilios = models.IntegerField(null=True, blank=True)
    nrhabitantes = models.IntegerField(null=True, blank=True)
    nrpregao = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = 'tbprocessourbano'

class Tbsituacaoprocesso(models.Model):
    id = models.AutoField(primary_key=True)
    nmsituacao = models.CharField(max_length=80, blank=True)
    dssituacao = models.TextField(blank=True)
    class Meta:
        db_table = 'tbsituacaoprocesso'

class Tbsituacaogeo(models.Model):
    id = models.AutoField(primary_key=True)
    nmsituacaogeo = models.CharField(max_length=80, blank=True)
    dssituacaogeo = models.TextField(blank=True)
    class Meta:
        db_table = 'tbsituacaogeo'

class Tbstatuspendencia(models.Model):
    id = models.AutoField(primary_key=True)
    stpendencia = models.IntegerField(null=True, blank=True)
    dspendencia = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return self.dspendencia
    class Meta:
        db_table = 'tbstatuspendencia'

class Tbsubarea(models.Model):
    id = models.AutoField(primary_key=True)
    cdsubarea = models.CharField(max_length=10, blank=True)
    nmsubarea = models.CharField(max_length=80, blank=True)
    def __unicode__(self):
        return self.nmsubarea
    class Meta:
        db_table = 'tbsubarea'

class Tbtipocaixa(models.Model):
    id = models.AutoField(primary_key=True)
    nmtipocaixa = models.CharField(max_length=80, blank=True)
    desctipocaixa = models.TextField(blank=True)
    def __unicode__(self):
        return self.nmtipocaixa
    class Meta:
        db_table = 'tbtipocaixa'

class Tbtipopendencia(models.Model):
    id = models.AutoField(primary_key=True)
    cdtipopend = models.IntegerField(null=True, blank=True)
    dspendencia = models.CharField(max_length=50, blank=True)
    cdgrupo = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = 'tbtipopendencia'

class Tbtipoprocesso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80, blank=True)
    tabela = models.CharField(max_length=50, blank=True)
    coridentificacao = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return self.nome
    class Meta:
        db_table = 'tbtipoprocesso'
        
class Tbservidor(models.Model):
    #idUser = models.ForeignKey('AuthUser')#models.IntegerField(primary_key=True)
    nmservidor = models.CharField(max_length=100, blank=True)
    nmunidade = models.CharField(max_length=100, blank=True)
    nmlotacao = models.CharField(max_length=30 , blank=True)
    cdSIAPE = models.CharField(max_length=7, null=True, blank=True)
    nrCPF = models.CharField(max_length=11, null=True, blank=True)
    dsportariacargo = models.CharField(max_length=80, null=True, blank=True)
    dsportaria  = models.CharField(max_length=80, null=True, blank=True)
    nmcargo  = models.CharField(max_length=40, null=True, blank=True)
    nrtelefone1 = models.CharField(max_length=10, null=True, blank=True)
    nrtelefone2  = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField (null=True, blank=True)
    dsatividades  = models.CharField(max_length=80, null=True)
    #def __unicode__(self):
    #    return self.nmservidor
    class Meta:
        db_table = 'tbservidor'

class Tbuf(models.Model):
    id = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=2, blank=True)
    nmuf = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'tbuf'

