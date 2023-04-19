from django.urls import path
from . import views


urlpatterns = [
    path('notes/', views.CreateNote.as_view(), name='notes'),
    path('is_archive/', views.Archive.as_view(), name='is_archive'),
    path('is_trash/', views.Trash.as_view(), name='is_trash')

]
