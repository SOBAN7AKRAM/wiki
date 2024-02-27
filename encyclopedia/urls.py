from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.displayEntry,name="entry"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newPage, name="newPage")
]
