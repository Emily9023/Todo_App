from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy

from .models import Task

class TaskList(generic.ListView):
    models = Task
    context_object_name = 'tasks'   # your own name for the list as a template variable
    queryset = Task.objects.filter() # Get 5 books containing the title war
    template_name = 'base/todo_list.html'  # Specify your own template name/location

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'   # your own name for the list as a template variable
    template_name = 'base/task.html'  # Specify your own template name/location

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') #go back to list

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks') #go back to list


class DeleteView(DeleteView):
    model = Task
    fields = '__all__'
    context_object_name = 'task'   # your own name for the list as a template variable
    success_url = reverse_lazy('tasks') #go back to list


