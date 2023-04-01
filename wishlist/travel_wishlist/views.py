from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(request): 

    if request.method == 'POST':
        # Create new place
        form = NewPlaceForm(request.POST) # Create form from data in request
        place = form.save() # Create new place object from data entered in form
        if form.is_valid(): # DB constraint validation
            place.save() # Save model to DB
            return redirect('place_list') # Refresh home page to display newly added places

    places = Place.objects.filter(visited=False).order_by('name') # Retrieve all objects from database where visited is False, order by name
    new_place_form = NewPlaceForm() # Empty form used to create HTML
    # Combine the template with dictionary containing places list and the place form to create a web page containing them together
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) 


def about(request):
    # About page containing author and description
    author = 'Natalie'
    about = 'A website to create a list of places to visit.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


def places_visited(request):
    # Page containing list of places that have already been visited
    visited = Place.objects.filter(visited=True) # Get all Place objects that have been checked as visited
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def place_was_visited(request, place_pk):
    # Allows user to change the value of a place object's 'visited' attribute to True
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk) # Get the object that corresponds to the requested primary key - send 404 response if pk doesn't exist
        place.visited = True # Change the object's visited value to True
        place.save()

    return redirect('place_list') # Reload to update list of places on home page