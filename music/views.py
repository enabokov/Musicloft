from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views import generic

from .forms import UserForm
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
    bands = Band.objects.all()
    albums = Album.objects.all()
    songs = Song.objects.all()

    context = {
        'bands': bands,
        'albums': albums,
        'songs': songs
    }

    return render(request, 'music/index.html', context)


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return index_view(request)
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)
