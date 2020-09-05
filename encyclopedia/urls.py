from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/edit/<str:TITLE>", views.edit_page, name="edit_page"),
    path("wiki/<str:TITLE>", views.entry_page, name="entry_page"),
    path("newpage", views.new_page, name="new_page"),
    path("randomPage", views.random_page, name="random_page"),
    path("search", views.search, name="search")
]
