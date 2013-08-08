from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home', name='home'),
    url(r'^web/rural', 'web.viewspublicas.rural'),
    url(r'^web/urbano', 'web.viewspublicas.urbano'),
    url(r'^sicop/consultas/', 'web.views.consultas'),
    url(r'^sicop/login/', 'django.contrib.auth.views.login', {"template_name":"sicop/login.html"}),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {"login_url":"/sicop/login/"}),
    # url(r'^web/$', 'web.views.txt', name='texto'),
    # url(r'^SICOP/', include('SICOP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^sicop/admin/', include(admin.site.urls)),
)