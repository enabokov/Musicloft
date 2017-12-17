from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic

from .forms import UserForm, LoginForm
from .models import Band, Album, LikedByUsers, BandGenres


class BandView(generic.DetailView):
    queryset = Band.objects.all()
    template_name = 'music/BandView.html'
    context_object_name = 'band'


class AlbumView(generic.DetailView):
    queryset = Album.objects.all()
    template_name = 'music/AlbumView.html'
    context_object_name = 'album'


class BandListView(generic.ListView):
    model = Band
    template_name = 'music/BandListView.html'
    context_object_name = 'bands'
    paginate_by = 30
    ordering = ['-popularity']


class AlbumListView(generic.ListView):
    model = Album
    template_name = 'music/AlbumListView.html'
    context_object_name = 'albums'

    def get_queryset(self):
        if 'pk' in self.kwargs.keys():
            band = get_object_or_404(Band, pk=self.kwargs['pk'])
            return Album.objects.filter(band=band)
        return Album.objects.all()


def index(request):
    form = UserForm(request.POST or None)
    bands = Band.objects.all().order_by('?')[:12]
    context = {
        'bands': bands,
        'form': form
    }
    return render(request, 'music/index.html', context)


def bands_list(request):
    bands = Band.objects.all().order_by('?')
    context = {
        'bands': bands,
    }
    return render(request, 'music/BandListView.html', context)


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


@login_required
def liked_bands(request):
    try:
        LikedByUsers.objects.create(
            user=request.user,
            band=Band.objects.get(pk=request.POST['band_id'])
        ).save()
    except IntegrityError:
        print('already exists')

    return redirect(reverse('music:bands'))


@login_required
def disliked_bands(request):
    LikedByUsers.objects.filter(
        user=request.user,
        band=Band.objects.get(pk=request.POST['band_id']),
    ).delete()
    return redirect(reverse('music:bands'))


@login_required
def liked(request):
    liked_bands = LikedByUsers.objects.filter(user=request.user).values_list('band', flat=True)
    bands = Band.objects.filter(id__in=liked_bands)
    context = {
        'bands': bands,
    }
    return render(request, 'music/user/liked.html', context=context)


@login_required
def recommendations(request):
    liked_bands = LikedByUsers.objects.filter(user=request.user).values_list('band', flat=True)
    bands = Band.objects.filter(id__in=liked_bands)

    liked_genres = []
    for liked in liked_bands:
        result = BandGenres.objects.filter(band=liked).values_list('genre', flat=True)
        liked_genres += result
    liked_genres = set(liked_genres)

    rank = []
    bands_id = Band.objects.all().values_list('id', flat=True)
    for band_id in bands_id:
        genres = BandGenres.objects.filter(band=band_id).values_list('genre', flat=True)
        rank.append((band_id, len(set(genres).intersection(liked_genres))))

    rank.sort(key=lambda x: x[1], reverse=True)
    ids = [x[0] for x in rank][:30]
    bands = Band.objects.filter(id__in=ids)

    return render(request, 'music/user/recommendations.html', context={'bands': bands})


# User information page
@login_required
def user_account(request):
    if not request.user.is_authenticated():
        return redirect(reverse('music:register'))
    else:
        context = {
            'username': request.user.username,
        }

        return render(request, 'music/user/account.html', context=context)


def search_band(request):
    results = None
    if request.method == 'POST' and request.POST['search_text']:
        search_text = request.POST['search_text']
        results = Band.objects.filter(name__contains=search_text)[:6:-1]

    return render(request, 'music/ajax_search.html', {'bands': results})
