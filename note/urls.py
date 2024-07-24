from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/note/create", views.create_note, name="create_note"),
    path("api/v1/note/update", views.update_note, name="update_note"),
    path("api/v1/note/delete", views.delete_note, name="delete_note"),
    path("api/v1/note/list", views.get_notes, name="get_notes"),
    path("api/v1/note/detail", views.get_note_detail, name="get_note_detail"),
    path("api/v1/note/category", views.get_categories, name="get_categories"),
    path("api/v1/note/search", views.search_notes_by_keyword, name="search_notes_by_keyword"),
]
