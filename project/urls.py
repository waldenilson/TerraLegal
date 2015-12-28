# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
project = 'project'

handler404 = project+'.core.views_excecoes.pagina_nao_encontrada'
handler403 = project+'.core.views_excecoes.permissao_negada'
handler500 = project+'.core.views_excecoes.erro_servidor'

urlpatterns = patterns('',

    # DAJAXICE AJAX DO PROJETO
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^livro/',include(project+'.livro.urls',namespace='livro')),
    url(r'^calculo/',include(project+'.calculo.urls',namespace='calculo')),
    url(r'^servidor/',include(project+'.servidor.urls',namespace='servidor')),
    url(r'^documento/',include(project+'.documento.urls',namespace='documento')),
    url(r'^web/',include(project+'.web.urls',namespace='web')),
    url(r'^core/',include(project+'.core.urls',namespace='core')),
    url(r'^geoinformacao/',include(project+'.geoinformacao.urls',namespace='geoinformacao')),
    url(r'^tramitacao/',include(project+'.tramitacao.urls',namespace='tramitacao')),

    # ACESSO AO PUBLICO
    url(r'^$', project+'.web.views_publicas.inicio'),
    url(r'^web/estatisticas/', project+'.web.estatisticas.estatisticas'),
    url(r'^web/mobile/', project+'.web.views_publicas.mobile'),
    url(r'^media/(?P<path>.*)$',project+'.tramitacao.util.media.download', {'document_root': settings.MEDIA_ROOT}),
   
    # GEOINFORMACOES
    url(r'^geo/glebas_federais/', project+'.tramitacao.restrito.geoinformacao.glebas_federais'),
    url(r'^geo/openlayers/', project+'.tramitacao.restrito.geoinformacao.openlayers'),
    
    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    #url(r'^admin/', include(admin.site.urls)),
    
)
