from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView
from .models import Post
# from users.forms import PostForm


     

def home(request) :
    context = {
        'posts' : Post.objects.all()
    }
    return render (request,'blog/home.html',context)

class RandomPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # Adjust this to your actual template path
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.all().order_by('?')
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/latest_posts.html' # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2    



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name ='blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # form_class = PostForm
    fields = ['title','content']

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    # form_class = PostForm
    fields = ['title','content']    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            f'u r not allowed to edit this post'

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
         

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False      


     


    


def about(request):
    return render (request,'blog/about.html',{'title':'About'}) 
