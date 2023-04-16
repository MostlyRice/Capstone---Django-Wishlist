from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from .forms import TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request): 

    if request.method == 'POST':
        # Create new place
        form = NewPlaceForm(request.POST) # Create form from data in request
        place = form.save(commit=False) # Create new place object from data entered in form
        place.user = request.user
        if form.is_valid(): # DB constraint validation
            place.save() # Save model to DB
            return redirect('place_list') # Refresh home page to display newly added places

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # Retrieve all objects from database where visited is False, order by name
    new_place_form = NewPlaceForm() # Empty form used to create HTML
    # Combine the template with dictionary containing places list and the place form to create a web page containing them together
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form}) 

@login_required
def about(request):
    # About page containing author and description
    author = 'Natalie'
    about = 'A website to create a list of places to visit.'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    # Page containing list of places that have already been visited
    visited = Place.objects.filter(visited=True) # Get all Place objects that have been checked as visited
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    # Allows user to change the value of a place object's 'visited' attribute to True
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk) # Get the object that corresponds to the requested primary key - send 404 response if pk doesn't exist
        if place.user == request.user:
            place.visited = True # Change the object's visited value to True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list') # Reload to update list of places on home page

@login_required
def place_details(request, place_pk):
    # Page containing details of a specific page
    place = get_object_or_404(Place, pk=place_pk)

    # Only display place if it belongs to logged in user
    if place.user != request.user:
        return HttpResponseForbidden
    
    # If POST request, capture data that was entered into the form and update the given place
    # Save the form if it's valid.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # TODO - Refine this 
        return redirect('place_details', place_pk=place_pk)
    else:  # If GET request, check if place is visited. 
        if place.visited:  # If visited, display form to user
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:  # If not visited, do not display form
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})
        


@login_required
def delete_place(request, place_pk):
    # Delete specific place
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user: # Ensure user owns the place selected
        place.delete() 
        return redirect('place_list') # Return to place list page
    else:
        HttpResponseForbidden() # Return 403 response if user doesn't own place