from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#def home(request):
#    return render(request, "home.html", {})
class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    #ordering = ['-id']
    ordering = ['-post_date']

class ArticleDetailView(DetailView):
    model= Post
    template_name = 'article_details.html'

class AddPostView(LoginRequiredMixin, CreateView):
    model= Post
    form_class = PostForm
    template_name = 'add_post.html'
    login_url = '/members/login/'

    #fields='__all__'
    #fields= ['title', 'body']

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'editpost.html'
    login_url = '/members/login/'
    #fields = ['title', 'body']

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    login_url = '/members/login/'
    success_url = reverse_lazy('home')
