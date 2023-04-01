from django.shortcuts import render, redirect
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':

        form = NewPlaceForm(request.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(visited=True).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request,'travel_wishlist/wishlist.html', {'places':places, 'new_place_form': new_place_form})

def places_visited(request):
    visited = Place.objects.filter(visited=False)
    return render(request, 'travel_wishlist/visted.html', {'visited':visited})

def about(request):
    author = 'James'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author':author, 'about':about})