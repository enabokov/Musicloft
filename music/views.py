from django.shortcuts import render
from django.views import generic

from .models import Band, Album, Song


class BandView(generic.ListView):
    model = Band
    template_name = 'music/BandView.html'
    context_object_name = 'bands'


class AlbumView(generic.ListView):
    model = Album
    template_name = 'music/AlbumView.html'
    context_object_name = 'albums'


def IndexView(request):
    bands = Band.objects.all()
    albums = Album.objects.all()
    songs = Song.objects.all()

    context = {
        'bands': bands,
        'albums': albums,
        'songs': songs
    }

    return render(request, 'music/index.html', context)
