from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        request.POST['author']= request.user.id
        return super(AddPostView, self).post(request, kwargs)


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'editpost.html'
    login_url = '/members/login/'


    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    login_url = '/members/login/'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

def CategoryView(request, cats):
    category_posts= Post.objects.filter(category= cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.replace('-', ' '), 'category_posts': category_posts})
