from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("wiki/<str:title>", views.view_entry, name="entry"),
    path("random", views.random, name="random")
]
