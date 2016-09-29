from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^bands/$', views.BandView.as_view(), name='bands'),
    url(r'^albums/$', views.AlbumView.as_view(), name='albums'),
]
