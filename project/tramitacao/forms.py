#coding:utf-8

# formularios customizados
from django.forms import models
from django import forms
from project.tramitacao.models import Tbpecastecnicas, Tbpregao,Tbprocessobase, Tbtipopendencia,\
    Tbtipocaixa, Tbcaixa, Tbsubarea, Tbgleba, Tbcontrato, Tbstatuspendencia,\
    Tbclassificacaoprocesso,\
    Tbtipoprocesso, Tbprocessorural, Tbprocessoclausula, Tbprocessourbano,\
    Tbsituacaoprocesso, Tbsituacaogeo, AuthGroup, Tbdivisao,\
    Tbpendencia, Tbmunicipio, Tbuf
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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
        
class FormCaixa(forms.ModelForm):
    class Meta:
        model = Tbcaixa

class FormDivisao(forms.ModelForm):
    class Meta:
        model = Tbdivisao
                        
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

# validadores

def ThreeLengthValidator(value):
    if len(value) <= 3:
        raise ValidationError('Informe no mínimo 3 caracteres.')


# construcao dos modelforms

class ContratoForm(forms.ModelForm):        
    nrcontrato = forms.CharField(
        label=str('Número do Contrato').decode('utf-8'),
        widget=forms.TextInput(
            attrs={
                'title':'Contrato'
            }
        )
    )
    nmempresa = forms.CharField(label='Nome da Empresa')
    class Meta:
        model = Tbcontrato
        exclude = ('tbdivisao',)
    def __init__(self,*args,**kwargs):
        super(ContratoForm,self).__init__(*args,**kwargs)
        self.fields['nmempresa'].validators.append(ThreeLengthValidator)


class PregaoForm(forms.ModelForm):        
    nrpregao = forms.CharField( label=str('Número do Pregão').decode('utf-8') )
    dspregao = forms.CharField(
        required = False,
        label=str('Descrição').decode('utf-8'),
        widget=forms.Textarea(
            attrs={
                'rows':'5'
            }
        )
    )
    class Meta:
        model = Tbpregao
        exclude = ('tbdivisao',)
    def __init__(self,*args,**kwargs):
        super(PregaoForm,self).__init__(*args,**kwargs)
        self.fields['nrpregao'].validators.append(ThreeLengthValidator)


class SubAreaForm(forms.ModelForm):        
    nmsubarea = forms.CharField(
        label=str('Nome').decode('utf-8')
    )
    class Meta:
        model = Tbsubarea
        exclude = ('cdsubarea','tbdivisao',)

class TipoCaixaForm(forms.ModelForm):        
    nmtipocaixa = forms.CharField(
        label=str('Nome').decode('utf-8')
    )
    desctipocaixa = forms.CharField(
        required = False,
        label=str('Descrição').decode('utf-8'),
        widget=forms.Textarea(
            attrs={
                'rows':'5'
            }
        )
    )
    class Meta:
        model = Tbtipocaixa


class GlebaForm(forms.ModelForm):        
    nmgleba = forms.CharField(
        label=str('Nome').decode('utf-8')
    )
    tbuf = forms.Select()
    tbsubarea = forms.Select()
    class Meta:
        model = Tbgleba
