from django.contrib import admin
from sicop.models import Tbtipocaixa, Tbtipoprocesso, Tbstatuspendencia,\
    Tbpecastecnicas, Tbclassificacaoprocesso, Tbsubarea, Tbconjuge, Tbcaixa,\
    Tbgleba, Tbcontrato, Tbsituacaoprocessourbano, Tbtipopendencia

# tbtipocaixa,
# tbcaixa,
# tbmunicipio, 
# tbtipopendencia,
# tbstatuspendencia, 
# tbsubarea, 
# tbconjuge,
# tbcontrato,
# tbgleba,
# tbsituacaoprocessourbano,
# tbclassificacaoprocesso,
# tbtipoprocesso

# TABELAS BASICAS (VARIAVEIS STATUS E/OU TIPOS)
admin.site.register(Tbtipoprocesso)
admin.site.register(Tbtipopendencia)
admin.site.register(Tbsituacaoprocessourbano)
admin.site.register(Tbclassificacaoprocesso)
admin.site.register(Tbstatuspendencia)
#admin.site.register(Tbpecastecnicas)

# TABELAS CONTROLE CRUD (MIGRACAO)
# admin.site.register(Tbmunicipio)
admin.site.register(Tbsubarea)
admin.site.register(Tbconjuge)
admin.site.register(Tbcontrato)
admin.site.register(Tbgleba)
admin.site.register(Tbcaixa)
admin.site.register(Tbtipocaixa)


