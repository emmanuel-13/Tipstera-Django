from django.urls import path

from . import views

urlpatterns = [
    path(
        'populate-areas/',
        views.populate_areas
    ),
    path(
        'populate-competitions/',
        views.populate_competitions
    ),
    path(
        'populate-teams/',
        views.populate_teams
    ),
    # path(
    #     'populate-matches/',
    #     views.populate_matches
    # ),
]