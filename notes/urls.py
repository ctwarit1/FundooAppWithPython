from django.urls import path
from . import views


urlpatterns = [
    # path('create_note/', views.create_note, name='create_note'),
    path('notes/', views.CreateNote.as_view(), name='notes'),
    path('is_archived/', views.Archive.as_view(), name='is_archived')

]
