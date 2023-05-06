from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from blog_psql.settings import EMAIL_HOST_USER
from django.views.decorators.http import require_POST
from taggit.models import Tag
# Create your views here.

def post_list(request, tag_slug=None):
    """Возвращает ответ text/html с постами со статусом 'PB' """
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'tag': tag})


def post_detail(request, year, month, day, post_slug):
    """Возвращает ответ text/html с одним опубликованным (status='PB') постом по его дате публикации
     и слогу"""
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post_slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комметариев
    comments = post.comments.filter(active=True)
    # Форма для ввода комментариев
    form = CommentForm()
    
    # Список схожих постов
    post_tags_ids = post.tag.values_list('id', flat=True)
    
    similar_posts = Post.published.filter(tag__in=post_tags_ids).exclude(id=post.id)
    
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     "form": form,
                                                     'similar_posts': similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} Рекомендует к прочтению {post.title}"
            message = f'К прочтению {post.title} at {post_url}\n\nКомментарий {cd["name"]} {cd["comments"]}'
            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})



















