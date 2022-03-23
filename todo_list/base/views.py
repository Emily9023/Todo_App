from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import generic
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin #restricts user from getting data unless logged in
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login #when register, logged in already

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm #built in form from django
    success_url = reverse_lazy('tasks') #go back to list

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        return super(RegisterPage, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, generic.ListView):
    models = Task
    context_object_name = 'tasks'   # your own name for the list as a template variable
    queryset = Task.objects.filter() # Get 5 books containing the title war
    template_name = 'base/todo_list.html'  # Specify your own template name/location

    #filters for the tasks for the authenticated user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context

    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'   # your own name for the list as a template variable
    template_name = 'base/task.html'  # Specify your own template name/location

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') #go back to list

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') #go back to list


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    fields = '__all__'
    context_object_name = 'task'   # your own name for the list as a template variable
    success_url = reverse_lazy('tasks') #go back to list


