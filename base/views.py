from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from.models import Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from base.models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

# Logiin view with user creation form didnt find another option    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = False
    success_url = reverse_lazy('tasks')

    #redirectt after registration
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    

    #for users that are logged in  not to view register page
    #def get (self, *args, **kwargs):
     #   if self.request.user.is_authenticated:
      #      return redirect('tasks')
       # return super(RegisterPage, self).get(*args, **kwargs)




class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

#For each user to get their own data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        #to implement ability to search a task
        search_input = self.request.GET.get('searching') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input
            )

        context['search_input'] = search_input    

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task    
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task  
    fields = ['title', 'description', 'complete']
    success_url  = reverse_lazy('tasks')

    

#to show the name of user when adding a task / separate the querysets of each
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)  

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task  
    fields = ['title', 'description', 'complete']
    success_url  = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task  
    context_object_name = 'task'
    success_url  = reverse_lazy('tasks')

def tasks_for_day(request, day):
    tasks = Task.objects.filter(day=day)
    return render(request, 'base/task_list.html', {'tasks': tasks})