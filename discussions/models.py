from django.db import models
from django.contrib.auth import get_user_model
from episodes.models import Episode

User = get_user_model()


class DiscussionThread(models.Model):
    """
    Модель темы для обсуждения в форуме
    Поддерживает полный CRUD
    """
    
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    
    content = models.TextField(
        verbose_name='Содержание'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discussion_threads',
        verbose_name='Автор'
    )
    
    episode = models.ForeignKey(
        Episode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='discussion_threads',
        verbose_name='Связанная серия'
    )
    
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Просмотры'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Тема обсуждения'
        verbose_name_plural = 'Темы обсуждений'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_comments_count(self):
        """Возвращает количество комментариев в теме"""
        return self.comments.count()
    
    def get_last_comment(self):
        """Возвращает последний комментарий в теме"""
        return self.comments.order_by('-created_at').first()
    

class Comment(models.Model):
    """
    Модель комментария к теме обсуждения.
    Поддерживает полный CRUD
    Поддерживает вложенные ответы (parent).
    """
    
    thread = models.ForeignKey(
        DiscussionThread,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Тема'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discussion_comments',
        verbose_name='Автор'
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    
    content = models.TextField(
        verbose_name='Текст комментария'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."
    
    def get_replies_count(self):
        """Возвращает количество ответов на комментарий"""
        return self.replies.count()
    
    def is_reply(self):
        """Проверяет, является ли комментарий ответом"""
        return self.parent is not None