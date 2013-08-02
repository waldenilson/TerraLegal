from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin: ALTERADO EDUARDO
#inclui linha
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/$', 'web.views.txt', name='texto'),
    # url(r'^SICOP/', include('SICOP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
