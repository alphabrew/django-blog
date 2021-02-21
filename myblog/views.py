from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

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

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


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

def LikeView(request, pk):
    post = get_object_or_404(Post, id= request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))
