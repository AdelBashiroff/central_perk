from django.db import models
from django.contrib.auth import get_user_model
from episodes.models import Episode

User = get_user_model()


class Review(models.Model):
    """
    Модель отзыва/рецензии на серию сериала.
    """
    
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
        (6, '6 - Очень хорошо'),
        (7, '7 - Великолепно'),
        (8, '8 - Идеально'),
        (9, '9 - Шедевр'),
        (10, '10 - Легендарно!'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Серия'
    )
    
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка'
    )
    
    text = models.TextField(
        verbose_name='Текст рецензии'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'episode']  # Пользователь может оставить только 1 отзыв на серию
    
    def __str__(self):
        return f"{self.user.username} - {self.episode.title} ({self.rating}/10)"