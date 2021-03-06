from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("query", views.search, name="query"),
    path("create", views.create, name="create"),
    path("randompage", views.randompage, name="randompage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.open, name="title")
]
