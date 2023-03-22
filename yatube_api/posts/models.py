from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return {self.title}


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Автор',
        null=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите картинку',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Пост'

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Пост',
        blank=True, null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Автор',
        null=True,
    )
    text = models.TextField(
        verbose_name='text to comment',
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:30]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='Юзер (Тот кто подписывается)',
        null=True,
    )
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='Автор(Тот на кого подписываются)',
        null=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('following', 'user'), name='unique_following'),
        )
