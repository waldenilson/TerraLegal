# formularios customizados
from django.forms import models
from web.models import Tbcaixa, Tbpecastecnicas, Tbprocesso, Tbprocessobase


class FormPecasTecnicas(models.ModelForm):
    class Meta:
        model = Tbpecastecnicas
        fields = ('tbcaixa','tbcontrato','nrentrega','nrcpfrequerente','nmrequerente','tbgleba','stpecatecnica',
                  'stanexadoprocesso','stenviadobrasilia','nrarea','nrperimetro','dsobservacao')
        
class FormProcessos(models.ModelForm):
    class Meta:
        model = Tbprocessobase
        fields = ('tbtipoprocesso','tbmunicipio','tbgleba','tbcaixa')