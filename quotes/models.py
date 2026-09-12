from django.db import models
from django.contrib.auth import get_user_model
from characters.models import Character
from episodes.models import Episode

User = get_user_model()


class Quote(models.Model):
    """
    Модель цитаты из сериала "Друзья".
    Поддерживает полный CRUD.
    """
    
    text = models.TextField(
        verbose_name='Текст цитаты'
    )
    
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name='Персонаж'
    )
    
    episode = models.ForeignKey(
        Episode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quotes',
        verbose_name='Серия'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name='Автор цитаты'
    )
    
    # Many-to-many для лайков
    likes = models.ManyToManyField(
        User,
        related_name='liked_quotes',
        blank=True,
        verbose_name='Лайки'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.character.name}: {self.text[:50]}..."
    
    def get_likes_count(self):
        """Возвращает количество лайков"""
        return self.likes.count()
    
    def get_comments_count(self):
        """Возвращает количество комментариев"""
        return self.comments.count()
    
    def is_liked_by_user(self, user):
        """Проверяет, лайкнул ли пользователь эту цитату"""
        if user.is_authenticated:
            return self.likes.filter(id=user.id).exists()
        return False