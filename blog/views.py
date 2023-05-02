from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def post_list(request):
    """Возвращает ответ text/html с постами со статусом 'PB' """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post_slug):
    """Возвращает ответ text/html с одним опубликованным (status='PB') постом по его дате публикации
     и слогу"""
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post_slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

