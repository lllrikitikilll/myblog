from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def post_list(request):
    """Возвращает ответ text/html с постами со статусом 'PB' """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, post_id):
    """Возвращает ответ text/html с одним опубликованным (status='PB') постом оп его 'id' """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})

