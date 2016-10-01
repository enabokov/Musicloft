from django.shortcuts import render
from django.views import generic

from .models import Band, Album, Song


class BandView(generic.DetailView):
    model = Band
    queryset = Band.objects.all()
    template_name = 'music/BandView.html'
    context_object_name = 'band'


class AlbumView(generic.DetailView):
    model = Album
    queryset = Album.objects.all()
    template_name = 'music/AlbumView.html'
    context_object_name = 'album'


class BandListView(generic.ListView):
    model = Band
    template_name = 'music/BandListView.html'
    context_object_name = 'bands'


class AlbumListView(generic.ListView):
    model = Album
    template_name = 'music/AlbumListView.html'
    context_object_name = 'albums'


def index_view(request):
    bands = Band.objects.all().order_by('?')[:12]
    albums = Album.objects.all().order_by('?')[:5]
    songs = Song.objects.all().order_by('?')[:10]



    context = {
        'bands': bands,
        'albums': albums,
        'songs': songs
    }

    return render(request, 'music/index.html', context)
