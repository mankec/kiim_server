from django.urls import path

from . import views

# app_name = "songs"
urlpatterns = [
    path("search/", views.search, name="search"),
]
