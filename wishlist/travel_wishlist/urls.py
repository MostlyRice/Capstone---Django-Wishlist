from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'), # Path leads to place_list function/page in views.py
    path('about', views.about, name='about'), # Path leads to about function/page in views.py
    path('visited', views.places_visited, name='places_visited'), # Path leads to visited function/page in views.py
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited') # Path will lead to view that will update a place object as visited
]