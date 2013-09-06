# formularios customizados
from django.forms import models
from django import forms
from sicop.models import Tbpecastecnicas, Tbprocessobase, Tbtipopendencia,\
    Tbtipocaixa, Tbcaixa, Tbsubarea, Tbgleba, Tbcontrato, Tbstatuspendencia,\
    Tbclassificacaoprocesso, Tbmunicipiomodulo,\
    Tbtipoprocesso, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano,\
    Tbsituacaoprocesso, Tbsituacaogeo


class FormPecasTecnicas(forms.ModelForm):
    class Meta:
        model = Tbpecastecnicas
        fields = ('tbcaixa','tbcontrato','nrentrega','nrcpfrequerente','nmrequerente','tbgleba','stpecatecnica',
                  'stanexadoprocesso','stenviadobrasilia','nrarea','nrperimetro','dsobservacao')

# ----PROCESSOS----------------------------------------------------------------------------------------------------------------------
class FormProcessoBase(models.ModelForm):
    class Meta:
        model = Tbprocessobase

class FormProcessoRural(models.ModelForm):
    class Meta:
        model = Tbprocessorural

class FormProcessoUrbano(models.ModelForm):
    class Meta:
        model = Tbprocessourbano

class FormProcessoClausula(models.ModelForm):
    class Meta:
        model = Tbprocessoclausula

# ----PROCESSOS----------------------------------------------------------------------------------------------------------------------
        
class FormTipoCaixa(models.ModelForm):
    class Meta:
        model = Tbtipocaixa
        
class FormCaixa(models.ModelForm):
    class Meta:
        model = Tbcaixa
        
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
        
class FormSituacaoProcesso(models.ModelForm):        
    class Meta:
        model = Tbsituacaoprocesso


class FormSituacaoGeo(models.ModelForm):        
    class Meta:
        model = Tbsituacaogeo
        