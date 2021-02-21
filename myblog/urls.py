
from django.urls import path
from . views import CategoryView
from . views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, LikeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='detail'),
    path('addpost', AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='edit_post'),
    path('article/delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>', CategoryView, name= 'category'),
    path('like/<int:pk>', LikeView, name= 'like_post'),
]
