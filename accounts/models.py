from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    Расширяет стандартного пользователя Django дополнительными полями.
    """
    
    CHARACTER_CHOICES = [
        ('rachel', 'Rachel Green'),
        ('monica', 'Monica Geller'),
        ('phoebe', 'Phoebe Buffay'),
        ('joey', 'Joey Tribbiani'),
        ('chandler', 'Chandler Bing'),
        ('ross', 'Ross Geller'),
    ]
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )
    
    favorite_character = models.CharField(
        max_length=20,
        choices=CHARACTER_CHOICES,
        blank=True,
        verbose_name='Любимый персонаж'
    )
    
    # Дополнительные поля для соцсети
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='friend_of',
        verbose_name='Друзья'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_friends_count(self):
        """Возвращает количество друзей"""
        return self.friends.count()
    
    def get_quotes_count(self):
        """Возвращает количество цитат, добавленных пользователем"""
        return self.quotes.count()
    
    def get_comments_count(self):
        """Возвращает количество комментариев, добавленных пользователем"""
        return self.comment_set.count()
    
    def get_unread_notifications_count(self):
        """Возвращает количество непрочитанных уведомлений"""
        return self.notifications.filter(is_read=False).count()