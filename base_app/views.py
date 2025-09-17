from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class Loginpage(LoginView):
    template_name='base_app/login.html'
    redirect_authenticated_user=True
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('tasks')

class Registerpage(FormView):
    template_name='base_app/register.html'
    redirect_authenticated_user=True
    form_class=UserCreationForm
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(Registerpage,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Registerpage,self).get(*args,**kwargs)

class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-value') or ''
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  

        context['count'] = queryset.filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-value') or ''
        return context


class Taskdetail(LoginRequiredMixin,DetailView):
    model= Task
    context_object_name='Task_name'

class Taskcreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','decription','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(Taskcreate,self).form_valid(form)

class Taskupdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','decription','complete']
    success_url=reverse_lazy('tasks')

class Taskdelete(LoginRequiredMixin,DeleteView):
    model=Task
    success_url=reverse_lazy('tasks')
    context_object_name = 'task'





