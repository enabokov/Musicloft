from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template import RequestContext
from django.views import generic

from .forms import UserForm, LoginForm
from .models import Band, Album, Song


class BandView(generic.DetailView):
    queryset = Band.objects.all()
    template_name = 'music/BandView.html'


class AlbumView(generic.DetailView):
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

    def get_queryset(self):
        if 'pk' in self.kwargs.keys():
            band = get_object_or_404(Band, pk=self.kwargs['pk'])
            return Album.objects.filter(band=band)
        return Album.objects.all()

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
                return redirect(reverse('music:account'))
    return render(request, 'music/user/registration.html', {'form': form})


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('music:account'))
            else:
                context = {'error_message': 'Your account has been blocked', 'form': form}
                return render(request, 'music/user/login.html', context)
        else:
            context = {'error_message': 'Incorrect login or password', 'form': form}
            return render(request, 'music/user/login.html', context)
    return render(request, 'music/user/login.html', {'form': form})


# Logout user and redirect to main page
def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect(reverse('music:index'))


# User information page
def user_account(request):
    if not request.user.is_authenticated():
        return redirect(reverse('music:register'))
    else:
        return render(request, 'music/user/account.html', content_type={'request': RequestContext(request)})
