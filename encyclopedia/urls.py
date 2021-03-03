from unicodedata import name
from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new_page", views.new_page, name="new_page"),
    path("wiki/edit", views.edit, name="edit"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/<str:name>", views.entry_page, name="entry_page")
]
