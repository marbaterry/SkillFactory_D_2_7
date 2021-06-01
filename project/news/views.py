from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.order_by('-date')


class PostDetail(DetailView):
    model = Post
    template_name = 'detailpost.html'
    context_object_name = 'post'
