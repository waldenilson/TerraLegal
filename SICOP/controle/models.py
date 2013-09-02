from django.db import models
# SISTEMAS DE CONTROLE 
# MODULO SERVIDORES/RH
class Tbservidor(models.Model):
    idUser = models.ForeignKey('AuthUser')#models.IntegerField(primary_key=True)
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
    dsatividades  = models.CharField(max_length=80)
    def __unicode__(self):
        return self.nmservidor
    class Meta:
        db_table = 'tbservidor'

