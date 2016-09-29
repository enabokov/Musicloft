from django.conf.urls import url

from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^band/(?P<pk>[0-9]+)/$', views.BandView.as_view(), name='band'),
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumView.as_view(), name='album'),
    url(r'^bands/$', views.BandListView.as_view(), name='bands'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),
]
