from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count
from ..models import Post
import markdown

register = template.Library()


# Возвращает количество постов
@register.simple_tag
def total_posts():
    count_noun = 'пост'  # окончание численных
    posts_count = Post.published.count()
    if posts_count % 10 in (2,3,4):
        count_noun = 'поста'
    elif posts_count % 10 in (5,6,7,8,9,0):
        count_noun = 'постов'
    return f'{posts_count} {count_noun}'

# Отрисовывает шаблон последних постов
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# Возвращает посты с наибольшим количеством комментариев
@register.simple_tag
def get_most_commented_posts(count=5):
    posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return posts

# Фильтр переводит текс согласно markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

