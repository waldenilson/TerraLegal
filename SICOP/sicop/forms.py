# formularios customizados
from django.forms import models
from django import forms
from sicop.models import Tbpecastecnicas, Tbprocessobase, Tbtipopendencia,\
    Tbtipocaixa, Tbcaixa


class FormPecasTecnicas(forms.ModelForm):
    class Meta:
        model = Tbpecastecnicas
        fields = ('tbcaixa','tbcontrato','nrentrega','nrcpfrequerente','nmrequerente','tbgleba','stpecatecnica',
                  'stanexadoprocesso','stenviadobrasilia','nrarea','nrperimetro','dsobservacao')
        
class FormProcessos(models.ModelForm):
    class Meta:
        model = Tbprocessobase
        fields = ('tbtipoprocesso','tbmunicipio','tbgleba','tbcaixa')
        
class FormTipoCaixa(models.ModelForm):
    class Meta:
        model = Tbtipocaixa
        fields = ('nmtipocaixa','desctipocaixa')
        
class FormCaixa(models.ModelForm):
    class Meta:
        model = Tbcaixa
        fields = ('nmlocalarquivo','tbtipocaixa')