from django.views import generic

from .models import Band, Album


class BandView(generic.ListView):
    template_name = 'music/BandView.html'
    context_object_name = 'bands'

    def get_queryset(self):
        return Band.objects.all()


class AlbumView(generic.ListView):
    template_name = 'music/AlbumView.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return Album.objects.all()
