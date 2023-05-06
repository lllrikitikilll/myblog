from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from taggit.managers import TaggableManager

# Create your models here.

# менеджер извлечения объектов из БД со статусом "PB"-"Опубликовано"
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Конкретно прикладной менеджер

    # choices status
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Черновик'
        PUBLISHED = 'PB', 'Опубликованно'

    # Content
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    body = models.TextField(verbose_name='Текст')
    # Time
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Status
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT, verbose_name='Статус')
    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts', verbose_name='Автор')  # Привязка постов к одному автору
    tag = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')  # Привязываем комментарии к одному посту
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'От {self.name}: {self.body}'
