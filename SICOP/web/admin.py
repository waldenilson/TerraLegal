from django.contrib import admin
from web.models import Tbtipocaixa, Tbmunicipio, Tbtipopendencia,\
    Tbstatuspendencia, Tbsubarea, Tbconjuge, Tbcontrato, Tbgleba,\
    Tbsituacaoprocessourbano, Tbclassificacaoprocesso, Tbtipoprocesso, Tbcaixa,\
    Tbprocessobase, Tbprocesso, Tbpecastecnicas

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
admin.site.register(Tbtipocaixa)
admin.site.register(Tbtipoprocesso)
# admin.site.register(Tbtipopendencia)
# admin.site.register(Tbsituacaoprocessourbano)
admin.site.register(Tbclassificacaoprocesso)
admin.site.register(Tbstatuspendencia)

# TABELAS CONTROLE CRUD (MIGRACAO)
# admin.site.register(Tbmunicipio)
# admin.site.register(Tbsubarea)
# admin.site.register(Tbconjuge)
# admin.site.register(Tbcontrato)
# admin.site.register(Tbgleba)
# admin.site.register(Tbcaixa)
