# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls import patterns, url, include
from django.conf import settings
admin.autodiscover()

project = 'project'

handler404 = project+'.core.views_excecoes.pagina_nao_encontrada'
handler403 = project+'.core.views_excecoes.permissao_negada'
handler500 = project+'.core.views_excecoes.erro_servidor'

urlpatterns = patterns('',

    # INDEX
    url(r'^$', project+'.web.views_publicas.inicio'),

    # APPS
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^livro/',include(project+'.livro.urls',namespace='livro')),
    url(r'^servidor/',include(project+'.servidor.urls',namespace='servidor')),
    url(r'^documento/',include(project+'.documento.urls',namespace='documento')),
    url(r'^web/',include(project+'.web.urls',namespace='web')),
    url(r'^core/',include(project+'.core.urls',namespace='core')),
    url(r'^geoinformacao/',include(project+'.geoinformacao.urls',namespace='geoinformacao')),
    url(r'^tramitacao/',include(project+'.tramitacao.urls',namespace='tramitacao')),

    # DIRETORIO MEDIA
    url(r'^media/(?P<path>.*)$',project+'.tramitacao.util.media.download', {'document_root': settings.MEDIA_ROOT}),

    # CONTROLE AUTENTICACAO
    url(r'^login/', 'django.contrib.auth.views.login', {"template_name":"index.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/"}),
    #url(r'^admin/', include(admin.site.urls)),

)
