'''
Created on 02/07/2014

@author: eduardo
'''
from django.forms import models
from django import forms
from servidor.models import Tbferias, Tbservidor

class FormServidor(forms.ModelForm):
    class Meta:
        model = Tbservidor
        fields = ('nmservidor','nmunidade','nmlotacao','cdsiape','nrcpf',
                  'dsportariacargo','dsportaria','nmcargo','nrtelefone1','nrtelefone2',
                  'email','dsatividades')
        
class FormFerias(forms.ModelForm):
    class Meta:
        model = Tbferias
        fields = ('nrAno','dtInicio1','nrDias1','dtInicio2','nrDias2','dtInicio3',
                  'nrDias3','stAntecipa','stDecimoTerceiro','stSituacao1')



