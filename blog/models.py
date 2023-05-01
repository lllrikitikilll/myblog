from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    # Time
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Status
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
