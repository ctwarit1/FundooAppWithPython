from django.urls import path
from . import views


urlpatterns = [
    path('notes/', views.CreateNote.as_view(), name='notes'),
    path('is_archive/', views.Archive.as_view(), name='is_archive'),
    path('is_trash/', views.Trash.as_view(), name='is_trash'),
    path('label/', views.Labels.as_view(), name='label'),
    path('label_with_notes/', views.LabelWithNotes.as_view(), name='label_with_notes'),
    path('collab_with_notes/', views.CollaboratorWithNotes.as_view(), name='collab_with_notes'),



]
