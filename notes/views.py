# notes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Note

# To list the user's notes
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by('-id')

# To create a new note
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# To update a note (owner only)
class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner

# To delete a note (owner only)
class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner

# To view all notes as an Admin
class AllNotesAdminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Note
    template_name = 'notes/all_notes.html'
    context_object_name = 'notes'

    def test_func(self):
        return self.request.user.is_superuser
    
@login_required
def profile(request):
    return render(request, 'notes/profile.html')    

# To register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})