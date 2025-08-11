from django.urls import path
from . import views
from .views import (
    NoteListView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    AllNotesAdminView,
    register,
    AllNotesAdminView,
)

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
    path('note/new/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('admin/all_notes/', AllNotesAdminView.as_view(), name='all_notes_admin'),
    path('register/', register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('all_notes/', AllNotesAdminView.as_view(), name='all_notes_admin'),
]