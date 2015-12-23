# formularios customizados
from django.forms import models
from django import forms
from TerraLegal.tramitacao.models import Tbpecastecnicas, Tbprocessobase, Tbtipopendencia,\
    Tbtipocaixa, Tbcaixa, Tbsubarea, Tbgleba, Tbcontrato, Tbstatuspendencia,\
    Tbclassificacaoprocesso,\
    Tbtipoprocesso, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano,\
    Tbsituacaoprocesso, Tbsituacaogeo, AuthGroup, Tbdivisao,\
    Tbpendencia, Tbmunicipio


class FormPecasTecnicas(forms.ModelForm):
    class Meta:
        model = Tbpecastecnicas
        fields = ('tbcaixa','tbcontrato','nrentrega','nrcpfrequerente','nmrequerente','tbgleba','stpecatecnica',
                  'stanexadoprocesso','stenviadobrasilia','nrarea','nrperimetro','dsobservacao')

# ----PROCESSOS----------------------------------------------------------------------------------------------------------------------
class FormProcessoBase(forms.ModelForm):
    class Meta:
        model = Tbprocessobase

class FormProcessoRural(forms.ModelForm):
    class Meta:
        model = Tbprocessorural

class FormProcessoUrbano(forms.ModelForm):
    class Meta:
        model = Tbprocessourbano

class FormProcessoClausula(forms.ModelForm):
    class Meta:
        model = Tbprocessoclausula

# ----PROCESSOS----------------------------------------------------------------------------------------------------------------------
        
class FormTipoCaixa(forms.ModelForm):
    class Meta:
        model = Tbtipocaixa
        
class FormCaixa(forms.ModelForm):
    class Meta:
        model = Tbcaixa

class FormDivisao(forms.ModelForm):
    class Meta:
        model = Tbdivisao
        
class FormSubArea(forms.ModelForm):
    class Meta:
        model = Tbsubarea
        fields = ('cdsubarea','nmsubarea','tbdivisao')
        
class FormGleba(forms.ModelForm):
    class Meta:
        model = Tbgleba
        fields = ('nmgleba', 'tbsubarea','tbuf')     
        
class FormPendencia(forms.ModelForm):        
    class Meta:
        model = Tbpendencia

class FormStatusPendencia(forms.ModelForm):
    class Meta:
        model = Tbstatuspendencia
        
class FormTipoPendencia(forms.ModelForm):        
    class Meta:
        model = Tbtipopendencia
        
class FormTipoProcesso(forms.ModelForm):
    class Meta:
        model = Tbtipoprocesso
        
class FormClassificacaoProcesso(forms.ModelForm):
    class Meta:
        model = Tbclassificacaoprocesso
        
class FormSituacaoProcesso(forms.ModelForm):        
    class Meta:
        model = Tbsituacaoprocesso


class FormSituacaoGeo(forms.ModelForm):        
    class Meta:
        model = Tbsituacaogeo
        
class FormAuthGroup(forms.ModelForm):
    class Meta:
        model = AuthGroup

class FormMunicipio(forms.ModelForm):
    class Meta:
        model = Tbmunicipio   


# construcao dos modelforms

class ContratoForm(forms.ModelForm):        
    class Meta:
        model = Tbcontrato
        exclude = ('tbdivisao',)