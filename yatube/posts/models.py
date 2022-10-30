from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('адрес', unique=True)
    description = models.TextField('описание')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField('текст поста')
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='автор'
    )
    group = models.ForeignKey(Group,
                              models.SET_NULL,
                              blank=True, null=True,
                              related_name='posts',
                              verbose_name='название группы',)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return f'{self.text[:15]}'
