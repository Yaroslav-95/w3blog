from django.conf.urls import url
from . import views

app_name = 'weblog'
urlpatterns = [
    url(r'^$', views.Index, name='Index'),
    url(r'^change-language/(?P<language>[-\w]+)/$', views.ChangeLanguage, name='ChangeLanguage'),
    url(r'^(?P<year>[0-9]{4})/$', views.Index, name='ArchiveIndex'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.Index, name='ArchiveIndex'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.Index, name='CategoryIndex'),
    url(r'^(?P<category_slug>[-\w]+)/(?P<post_slug>[-\w]+)/$', views.PostView, name='PostView'),
]