from django.conf.urls import url

from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # User urls
    url(r'^registration/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^account/$', views.user_account, name='account'),
    # Data urls
    url(r'^bands/$', views.bands_list, name='bands'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),  # All albums
    url(r'^band/(?P<pk>[0-9]+)/$', views.BandView.as_view(), name='band'),
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumView.as_view(), name='album'),
    url(r'^albums/(?P<pk>[0-9]+)/$', views.AlbumListView.as_view(), name='albums'),  # Albums for precise band
    # Test search
    url(r'^search/$', views.search_band, name='search'),
]