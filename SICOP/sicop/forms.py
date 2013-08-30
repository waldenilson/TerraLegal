# formularios customizados
from django.forms import models
from django import forms
from sicop.models import Tbpecastecnicas, Tbprocessobase, Tbtipopendencia,\
    Tbtipocaixa, Tbcaixa, Tbsubarea, Tbgleba, Tbcontrato, Tbstatuspendencia,\
    Tbsituacaoprocessourbano, Tbclassificacaoprocesso, Tbmunicipiomodulo,\
    Tbtipoprocesso


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
        
class FormSubArea(models.ModelForm):
    class Meta:
        model = Tbsubarea
        fields = ('cdsubarea','nmsubarea')
        
class FormGleba(models.ModelForm):
    class Meta:
        model = Tbgleba
        fields = ('nmgleba', 'tbsubarea')     
        
class FormContrato(models.ModelForm):        
    class Meta:
        model = Tbcontrato

class FormStatusPendencia(models.ModelForm):
    class Meta:
        model = Tbstatuspendencia
        
class FormTipoPendencia(models.ModelForm):        
    class Meta:
        model = Tbtipopendencia

class FormTipoProcesso(models.ModelForm):
    class Meta:
        model = Tbtipoprocesso
        
class FormMunicipioModulo(models.ModelForm):        
    class Meta:
        model = Tbmunicipiomodulo

class FormClassificacaoProcesso(models.ModelForm):
    class Meta:
        model = Tbclassificacaoprocesso
        
class FormSituacaoProcessoUrbano(models.ModelForm):        
    class Meta:
        model = Tbsituacaoprocessourbano
           
        