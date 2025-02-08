from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel, CreatedAtdModel
from .constants import MAX_LENGTH, SLICE_LENGTH

User = get_user_model()


class Category(PublishedModel, CreatedAtdModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок',
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=False
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:SLICE_LENGTH]


class Location(PublishedModel, CreatedAtdModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места',
        blank=False
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:SLICE_LENGTH]


class Post(PublishedModel, CreatedAtdModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок',
        blank=False
    )
    text = models.TextField(
        verbose_name='Текст',
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        blank=False,
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Категория',
        null=True
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:SLICE_LENGTH]


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"Комментарий от {self.author} к посту {self.post}"
