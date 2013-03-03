from django.conf.urls import patterns, include, url
from django.contrib import admin

from make_mozilla.pages import views

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(.+)/$', views.serve, name='page'),
)
