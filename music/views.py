from django.shortcuts import render
from .models import Band
from django.views import generic

# Create your views here.


class BandView(generic.ListView):
    template_name = 'music/BandView.html'
    context_object_name = 'bands'

    def get_queryset(self):
        return Band.objects.all()