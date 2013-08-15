# formularios customizados
from django.forms import models
from web.models import Tbcaixa, Tbpecastecnicas


class FormPecasTecnicas(models.ModelForm):
    class Meta:
        model = Tbpecastecnicas
        fields = ('tbcaixa','tbcontrato','tbgleba','stenviadobrasilia','nrarea','nrperimetro','dsobservacao')