from django.db import models
from sicop.models import AuthUser
# SISTEMAS DE CONTROLE 
# MODULO SERVIDORES/RH

class Tbservidor(models.Model):
    id = models.AutoField(primary_key=True)
    iduser = models.ForeignKey(AuthUser, db_column='idUser_id') # Field name made lowercase.
    nmservidor = models.CharField(max_length=100)
    nmunidade = models.CharField(max_length=100)
    nmlotacao = models.CharField(max_length=30)
    cdsiape = models.CharField(max_length=7, db_column='cdSIAPE', blank=True) # Field name made lowercase.
    nrcpf = models.CharField(max_length=11, db_column='nrCPF', blank=True) # Field name made lowercase.
    dsportariacargo = models.CharField(max_length=80, blank=True)
    dsportaria = models.CharField(max_length=80, blank=True)
    nmcargo = models.CharField(max_length=40, blank=True)
    nrtelefone1 = models.CharField(max_length=10, blank=True)
    nrtelefone2 = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=75, blank=True)
    dsatividades = models.CharField(max_length=80)
    class Meta:
        db_table = 'tbservidor'


